package model;

import com.google.gson.Gson;
import com.rabbitmq.client.*;
import lombok.*;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.TimeoutException;

@Data
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class CmpECoinValidatorNode implements Runnable {
    //CmpECoinNetwDispatcher netwDispatcherAddress;
    CmpEBlockchain blockChain;
    List<CmpETransaction> listenQForTransactionsFromNetwDispatcher;
    List<CmpEBlock> listenQForValidatedBlocksFromNetwDispatcher;
    CmpECoinWallet wallet;
    String publicAddress;

    private final String QUEUE_DISPATCHER_TO_VALIDATOR;
    private static final String EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR = "Dispatcher2ValidatorExchange";
    private final static String QUEUE_VALIDATOR_TO_DISPATCHER = "Validator2Dispatcher";
    private final ConnectionFactory factory;
    private final Channel channel;
    private final Connection connection;
    private final String name;

    public CmpECoinValidatorNode(String name,String publicAddress,CmpECoinWallet wallet) throws IOException, TimeoutException {
        this.name = name;
        this.wallet=wallet;
        this.publicAddress=publicAddress;

        this.factory = new ConnectionFactory();
        this.factory.setHost("localhost");
        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.exchangeDeclare(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "fanout");
        this.QUEUE_DISPATCHER_TO_VALIDATOR = this.channel.queueDeclare().getQueue();
        this.channel.queueBind(this.QUEUE_DISPATCHER_TO_VALIDATOR, EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "");

        this.channel.queueDeclare(QUEUE_VALIDATOR_TO_DISPATCHER, false, false, false, null);


    }

    @SneakyThrows
    @Override
    public void run() {

        // Whenever validator gets a message from the dispatcher, this callback is called
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            try {
                dispatcherMessageHandle(message);
            } catch (TimeoutException e) {
                e.printStackTrace();
            }
        };
        channel.basicConsume(this.QUEUE_DISPATCHER_TO_VALIDATOR, true, deliverCallback, consumerTag -> { });

        this.connection.addShutdownListener(new ShutdownListener() {
            public void shutdownCompleted(ShutdownSignalException cause)
            {
                System.out.println(cause.getReason());
            }
        });

        joinCmpECoinNetw();
    }

    // When validator wants to send a message to Dispatcher, it calls this method
    private void sendMessageToDispatcher(String message) throws IOException, TimeoutException {
        try {
            channel.basicPublish("", QUEUE_VALIDATOR_TO_DISPATCHER, null, message.getBytes());
            System.out.println(message);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /*
     * Message is processed, request is determined.
     * Request is handled
     * After the operation, sendMessageToDispatcher can be called
     */
    private void dispatcherMessageHandle(String message) throws IOException, TimeoutException {
        Message msgObj = new Gson().fromJson(message, Message.class);
        System.out.println("Validator:" + this.name  + msgObj.getContent() + " " + msgObj.getType() + " " + msgObj.getBlock()  + " " + msgObj.getJoinedNodeAddresses()  + " " + msgObj.getChain());

        switch(msgObj.getType()) {
            case Transaction:
                this.handleReceivedTransactions(msgObj.getTransaction());
                break;
            case ValidatedBlock:
                this.handleReceivedValidatedBlock(msgObj.getBlock());
                break;
            case Beacon:
                this.handleBeaconAndStartValidationProc();
                break;
            case JoinedNodeAddresses:
                this.updateChain(msgObj.getChain());
                break;
            default:
                System.out.println("Validator:" + this.name  + "Unknown msg type: "+msgObj.getType());
        }
    }

    private void updateChain(CmpEBlockchain chain) {
        this.setBlockChain(chain);
    }

    //Sends join message to network dispatcher
    public void joinCmpECoinNetw() throws IOException, TimeoutException {
        Message msgObj = Message.builder().type(MessageType.ValidatorJoin).content(this.name+" joined!").validatorNodeAddress(this.publicAddress).build();
        System.out.println("Validator:" + this.name + ":" + this.publicAddress +  " requested to join the network.");
        String msgToBeSent = new Gson().toJson(msgObj);
        this.sendMessageToDispatcher(msgToBeSent);
    }

    public void handleReceivedTransactions(CmpETransaction transaction) {
        if (transaction.isTransactionValid()){
            listenQForTransactionsFromNetwDispatcher.add(transaction);
        }
        else{
            System.out.println("Validator:" + this.name  + " Received transaction is invalid.");
        }
    }

    public void handleReceivedValidatedBlock(CmpEBlock block) {
        if (block.hasValidTransactions()){
            this.listenQForValidatedBlocksFromNetwDispatcher.add(block);
        }
        else{
            System.out.println("Validator:" + this.name  + " Received block is invalid.");
        }
    }

    public void handleBeaconAndStartValidationProc() throws IOException, TimeoutException {
        //Adding block mining reward
        CmpETransaction transaction = CmpETransaction.builder().amount(1L).toAddress(publicAddress).build();
        transaction.signTransaction(wallet.getPrivateKey());
        listenQForTransactionsFromNetwDispatcher.add(transaction);

        //Building the block
        CmpEBlock block = CmpEBlock.builder()
                .prevBlockHash(blockChain.getChain().get(blockChain.getChain().size() - 1).getCurrBlockHash())
                .timestamp(System.currentTimeMillis())
                .transactions(listenQForTransactionsFromNetwDispatcher)
                .build();  // Corresponding constructor has to call POW calculation and Current Block Hash from these values
        block.validateBlock();

        //Sending the block
        Message msgObj = Message.builder().type(MessageType.ValidatedBlock).block(block).build();
        String msgToBeSent = new Gson().toJson(msgObj);
        this.sendMessageToDispatcher(msgToBeSent);
        //TODO netwDispatcherAddress.validatedBlockRcvQ.add(block);
    }
}

