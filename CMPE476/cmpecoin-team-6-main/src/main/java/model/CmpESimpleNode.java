package model;

import com.google.gson.Gson;
import com.rabbitmq.client.*;
import lombok.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeoutException;

@Data
public class CmpESimpleNode implements Runnable {
//    CmpECoinNetwDispatcher netwDispatcherAddress;
    CmpEBlockchain blockChain;
    List<CmpEBlock> listenQForValidatedBlocksFromNetwDispatcher;
    CmpECoinWallet wallet;
    private final String name;
    String publicAddress;

    final static Long meanTransactionInterDuration = 1000L;

    private final ConnectionFactory factory;
    private final Channel channel;
    private final Connection connection;
    private List<String> joinedNodeAddresses = new ArrayList<>(); // bunu almak lazim
    private final String QUEUE_DISPATCHER_TO_SIMPLENODE;
    private final static String QUEUE_SIMPLENODE_TO_DISPATCHER = "SimpleNode2Dispatcher";
    private static final String EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE = "Dispatcher2SimpleNodeExchange";

    public CmpESimpleNode(String name,String publicAddress,CmpECoinWallet wallet) throws IOException, TimeoutException {
        this.name = name;
        this.wallet=wallet;
        this.publicAddress=publicAddress;
        this.factory = new ConnectionFactory();
        this.factory.setHost("localhost");
        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.exchangeDeclare(EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE, "fanout");
        this.QUEUE_DISPATCHER_TO_SIMPLENODE = this.channel.queueDeclare().getQueue();
        this.channel.queueBind(this.QUEUE_DISPATCHER_TO_SIMPLENODE, EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE, "");

        this.channel.queueDeclare(QUEUE_SIMPLENODE_TO_DISPATCHER, false, false, false, null);
    }

    public void handleReceivedValidatedBlock(CmpEBlock block) {
        if (block.hasValidTransactions())
            this.listenQForValidatedBlocksFromNetwDispatcher.add(block);
    }

    @SneakyThrows
    public void listenValidatorQueue() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        DeliverCallback validatedBlockMessageCallback = (consumerTag, delivery) -> {
            String body = new String(delivery.getBody(), "UTF-8");
            Message message = new Gson().fromJson(body, Message.class);
            if(message.getType().equals(MessageType.ValidatedBlock)) {
                handleReceivedValidatedBlock(message.getBlock());
            }
        };
        channel.basicConsume(QUEUE_DISPATCHER_TO_SIMPLENODE, true, validatedBlockMessageCallback, consumerTag -> { });
    }
    @SneakyThrows
    public void joinCmpECoinNetw() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();
        Message msgObj = Message.builder().type(MessageType.NodeJoin).simpleNodeAddress(wallet.getPublicKey()).build();
        String msgToBeSent = new Gson().toJson(msgObj);
        channel.basicPublish("",  QUEUE_SIMPLENODE_TO_DISPATCHER, null, msgToBeSent.getBytes());
    }

    public void doRandomTransactions() throws InterruptedException {
        Random rand = new Random();
        // Alt tarafi yeni bir thread olusturup cagir;

        while(true) {
            Thread.sleep((long) (Math.log(1-rand.nextDouble())/(-meanTransactionInterDuration)));
            while(wallet.getCurrentBalance()==0);
            Long amount = (rand.nextLong()%wallet.getCurrentBalance()) + 1;
            int ran = rand.nextInt(joinedNodeAddresses.size());
            CmpETransaction transaction = CmpETransaction.builder()
                    .timestamp(System.currentTimeMillis())
                    .amount(amount)
                    .fromAddress(wallet.getPublicKey())
                    .toAddress(joinedNodeAddresses.get(ran))
                    .build();
            transaction.signTransaction(wallet.getPrivateKey());
            sendTransactionToDispatcher(transaction);
        }
    }

    @SneakyThrows
    private void sendTransactionToDispatcher(CmpETransaction transaction) {
        Message msgObj = Message.builder().type(MessageType.Transaction).transaction(transaction).build();
        String msgToBeSent = new Gson().toJson(msgObj);
        channel.basicPublish("",  QUEUE_SIMPLENODE_TO_DISPATCHER, null, msgToBeSent.getBytes());
    }

    public void doRandomInvalidTransactions() throws InterruptedException {
        Random rand = new Random();
        // Alt tarafi yeni bir thread olusturup cagir;
        while(true) {
            Thread.sleep((long) (Math.log(1-rand.nextDouble())/(-meanTransactionInterDuration)));
            while(wallet.getCurrentBalance()==0);
            Long amount = (rand.nextLong()%wallet.getCurrentBalance()) + 1;
            CmpETransaction transaction = CmpETransaction.builder()
                    .timestamp(System.currentTimeMillis())
                    .amount(amount)
                    .fromAddress(wallet.getPublicKey())
                    .toAddress(joinedNodeAddresses.get(rand.nextInt()%joinedNodeAddresses.size()))
                    .build();
            transaction.signTransaction("INVALIDSECRETKEY");
            // TODO: add other invalid options
        }
    }

    /*
     * Message is processed, request is determined.
     * Request is handled
     * After the operation, sendMessageToDispatcher can be called
     */
    private void dispatcherMessageHandle(String message) throws IOException, TimeoutException {
        Message msgObj = new Gson().fromJson(message, Message.class);

        switch(msgObj.getType()) {
//            case Transaction:
//                this.handleReceivedTransactions(msgObj.getTransaction());
//                break;
//            case ValidatedBlock:
//                this.handleReceivedValidatedBlock(msgObj.getBlock());
//                break;
//            case Beacon:
//                this.handleBeaconAndStartValidationProc();
//                break;
            case JoinedNodeAddresses:
                System.out.println("Simple Node:" + this.name  + msgObj.getJoinedNodeAddresses());
                this.updateChainAndNodes(msgObj.getChain(), msgObj.getJoinedNodeAddresses());
                break;
            default:
                System.out.println("Unknown msg type: "+msgObj.getType());
        }
    }

    private void updateChainAndNodes(CmpEBlockchain chain, List<String> joinedNodeAddresses){
        if(this.getBlockChain() == null) {
            this.setBlockChain(chain);
        }
        this.setJoinedNodeAddresses(joinedNodeAddresses);
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
        channel.basicConsume(this.QUEUE_DISPATCHER_TO_SIMPLENODE, true, deliverCallback, consumerTag -> { });

        this.connection.addShutdownListener(new ShutdownListener() {
            public void shutdownCompleted(ShutdownSignalException cause)
            {
                System.out.println(cause.getReason());
            }
        });

        joinCmpECoinNetw();
    }
}

