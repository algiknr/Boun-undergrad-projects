package model;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

public class CmpEWalletTest {
    @Test
    void calculateCurrBlockHashTEST() {

        CmpECoinWallet cmpECoinWallet = CmpECoinWallet.builder().build();
        cmpECoinWallet.generateKeyPair();

        assertThat(cmpECoinWallet.getPublicKey()).isNotEmpty();
        assertThat(cmpECoinWallet.getPrivateKey()).isNotEmpty();
    }
}
