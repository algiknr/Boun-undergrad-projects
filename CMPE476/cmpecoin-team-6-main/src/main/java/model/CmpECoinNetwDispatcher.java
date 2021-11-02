package model;

import java.io.*;

import com.google.gson.Gson;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DeliverCallback;
import lombok.SneakyThrows;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;
import com.rabbitmq.client.ShutdownSignalException;
import com.rabbitmq.client.ShutdownListener;

public class CmpECoinNetwDispatcher implements Runnable{

    private List<CmpETransaction> transxRcvQ;
    private List<CmpEBlock> validatedBlockRcvQ;
    private List<String> joinedNodeAddresses;
    private CmpEBlockchain chain;
    private final ConnectionFactory factory;
    private final Connection connection;
    private final Channel channel;
    private static final String EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR = "Dispatcher2ValidatorExchange";
    private static final String EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE = "Dispatcher2SimpleNodeExchange";
    private final static String QUEUE_VALIDATOR_TO_DISPATCHER = "Validator2Dispatcher";
    private final static String QUEUE_SIMPLENODE_TO_DISPATCHER = "SimpleNode2Dispatcher";
    private final static Gson gson = new Gson();

    public CmpECoinNetwDispatcher() throws IOException, TimeoutException {
        transxRcvQ = new ArrayList<>();
        validatedBlockRcvQ = new ArrayList<>();
        joinedNodeAddresses = new ArrayList<>();
        this.factory = new ConnectionFactory();
        this.factory.setHost("localhost");
        this.chain = new CmpEBlockchain();
        this.chain.createInitialDummyBlock();
        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.exchangeDeclare(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "fanout");
        this.channel.exchangeDeclare(EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE, "fanout");
        this.channel.queueDeclare(QUEUE_VALIDATOR_TO_DISPATCHER, false, false, false, null); // Gets Validator's messages
        this.channel.queueDeclare(QUEUE_SIMPLENODE_TO_DISPATCHER, false, false, false, null); // Gets Simple Node's messages
    }

    private void broadcastReceivedTransx() throws IOException {
        Message message = Message.builder().type(MessageType.Transaction).transactions(transxRcvQ).build();
        String msgObj = gson.toJson(message);
        this.channel.basicPublish(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "", null, msgObj.getBytes("UTF-8"));
    }

    private void broadcastLastValidatedBlock() throws IOException {
        Message message = Message.builder().type(MessageType.ValidatedBlock).block(validatedBlockRcvQ.get(0)).build();
        String msgObj = gson.toJson(message);
        this.channel.basicPublish(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "", null, msgObj.getBytes("UTF-8"));
    }

    private void broadcastValidationBeacon() throws IOException {
        Message message = Message.builder().type(MessageType.Beacon).build();
        String msgObj = gson.toJson(message);
        this.channel.basicPublish(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "", null, msgObj.getBytes("UTF-8"));
    }
//
//    public CmpEBlockchain sendCurrentBlockChainTo(String address){
//        return chain;
//    }
//
//    public List<String> sendSimpleNodeAddresses(){
//        return joinedNodeAddresses;
//    }

    @SneakyThrows
    @Override
    public void run() {
        // Validator's messages will be met here
        DeliverCallback validatorMessageCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            handleValidatorMessage(message);
        };
        this.channel.basicConsume(QUEUE_VALIDATOR_TO_DISPATCHER, true, validatorMessageCallback, consumerTag -> { });

        // Simple Node's messages will be met here
        DeliverCallback simpleNodeMessageCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            handleSimpleNodeMessage(message);
        };
        this.channel.basicConsume(QUEUE_SIMPLENODE_TO_DISPATCHER, true, simpleNodeMessageCallback, consumerTag -> { });

        this.channel.addShutdownListener(new ShutdownListener() {
            public void shutdownCompleted(ShutdownSignalException cause)
            {
                System.out.println(cause.getCause());
            }
        });
        /*
        * Dispatcher will send beacons every 5 seconds
        */
        while(true) {
            Thread.sleep(5000);
            broadcastValidationBeacon();
            System.out.println("[Dispatcher] Beacon sent");
        }
    }

    private void handleValidatorMessage(String message) throws IOException {
        Message msgObj = gson.fromJson(message, Message.class);
        if(msgObj.getType().equals(MessageType.ValidatorJoin)){
            joinedNodeAddresses.add(msgObj.getValidatorNodeAddress()); // content is Public Key
            System.out.println(msgObj.getValidatorNodeAddress() +  " joined the network.");
            publishNewJoinedNode();
        } else if(msgObj.getType().equals(MessageType.ValidatedBlock)){
            CmpEBlock block = msgObj.getBlock();
            validatedBlockRcvQ.add(block);
            broadcastLastValidatedBlock();
        }
    }

    private void handleSimpleNodeMessage(String message) throws IOException {
        Message msgObj = gson.fromJson(message, Message.class);
        if(msgObj.getType().equals(MessageType.NodeJoin)){
            joinedNodeAddresses.add(msgObj.getSimpleNodeAddress()); // content is Public Key
            System.out.println(msgObj.getSimpleNodeAddress() +  " joined the network.");
            publishNewJoinedNode();
        } else if(msgObj.getType().equals(MessageType.Transaction)){
            List<CmpETransaction> transactions = msgObj.getTransactions();
            transxRcvQ.addAll(transactions);
            broadcastReceivedTransx();
        }
    }

    private void publishNewJoinedNode() throws IOException {
        Message msgObj = Message.builder().type(MessageType.JoinedNodeAddresses).joinedNodeAddresses(joinedNodeAddresses).chain(chain).build();
        String msgToBeSent = new Gson().toJson(msgObj);
        this.channel.basicPublish(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "", null, msgToBeSent.getBytes("UTF-8"));
        this.channel.basicPublish(EXCHANGE_NAME_DISPATCHER_TO_SIMPLENODE, "", null, msgToBeSent.getBytes("UTF-8"));
    }
}
