import model.*;

import java.security.KeyPair;

public class App {

    public static void main(String[] argv) throws Exception {

        Thread dispatcherThread = new Thread(new CmpECoinNetwDispatcher());
        dispatcherThread.start();

        Thread.sleep(2000);

        CmpECoinWallet wallet1 = CmpECoinWallet.builder().currentBalance(122L).build();
        wallet1.generateKeyPair();

        Thread validatorNode = new Thread(new CmpECoinValidatorNode("node1", wallet1.getPublicKey(),wallet1));
        validatorNode.start();

        CmpECoinWallet wallet2 = CmpECoinWallet.builder().currentBalance(122L).build();
        wallet2.generateKeyPair();
        CmpESimpleNode simpleNode = new CmpESimpleNode("node2", wallet2.getPublicKey(), wallet2);
        Thread simpleNodeThread = new Thread(simpleNode);
        simpleNodeThread.start();

//        dispatcherThread.join();
//        validatorNode.join();

//        simpleNodeThread.join();

        System.out.println("Initializations are Done");

        Thread.sleep(2000);
        simpleNode.doRandomTransactions();
    }
}
