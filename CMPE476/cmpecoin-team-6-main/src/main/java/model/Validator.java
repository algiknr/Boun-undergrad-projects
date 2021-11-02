package model;

import com.google.gson.Gson;
import com.rabbitmq.client.*;
import lombok.SneakyThrows;
import org.assertj.core.error.ShouldHaveSameSizeAs;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Validator implements Runnable{

    private final String QUEUE_DISPATCHER_TO_VALIDATOR;
    private static final String EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR = "Distpatcher2ValidatorExchange";
    private final static String QUEUE_VALIDATOR_TO_DISPATCHER = "Validator2Distpatcher";
    private final ConnectionFactory factory;
    private final Channel channel;
    private final Connection connection;
    private final String name;

    public Validator(String name) throws IOException, TimeoutException {
        this.name = name;
        this.factory = new ConnectionFactory();
        this.factory.setHost("localhost");
        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.exchangeDeclare(EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "fanout");
        this.QUEUE_DISPATCHER_TO_VALIDATOR = this.channel.queueDeclare().getQueue();
        this.channel.queueBind(this.QUEUE_DISPATCHER_TO_VALIDATOR, EXCHANGE_NAME_DISPATCHER_TO_VALIDATOR, "");
    }

    @SneakyThrows
    @Override
    public void run() {

        // Whenever validator gets a message from the dispatcher, this callback is called
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            dispatcherMessageHandle(message);
        };
        channel.basicConsume(this.QUEUE_DISPATCHER_TO_VALIDATOR, true, deliverCallback, consumerTag -> { });
    }

    /*
    * Message is processed, request is determined.
    * Request is handled
    * After the operation, sendMessageToDispatcher can be called
    */
    private void dispatcherMessageHandle(String message){
        Message msgObj = new Gson().fromJson(message, Message.class);
        System.out.println(msgObj.getContent() + " " + msgObj.getType() + " " + msgObj.getBlock());
//        System.out.println(" [" + this.name +"] Received '" + message + "'");
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
}
