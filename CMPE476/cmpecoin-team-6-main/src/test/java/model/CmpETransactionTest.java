package model;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import service.CmpeUtil;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

@ExtendWith(MockitoExtension.class)
class CmpETransactionTest {

    @Test
    void calculateTransactionHash() {
        CmpETransaction cmpETransaction = CmpETransaction.builder()
                .fromAddress("fa")
                .amount(1L)
                .timestamp(5L)
                .toAddress("jj")
                .build();
        String trans=cmpETransaction.calculateTransactionHash();
        assertThat(trans).isNotEmpty();
        assertThat(trans).isEqualTo(CmpeUtil.hash("fa/jj/1/5"));
    }

    @Test
    void signTransaction() {
    }

    @Test
    void isTransactionValid() throws NoSuchAlgorithmException {

        SecureRandom secureRandom = new SecureRandom();
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048, secureRandom);
        KeyPair keyPair = keyPairGenerator.generateKeyPair();

        CmpETransaction cmpETransaction = CmpETransaction.builder()
                .fromAddress(CmpeUtil.getStringFromKey(keyPair.getPublic()))
                .amount(5L)
                .timestamp(4L)
                .toAddress("toAddress")
                .build();

        cmpETransaction.signTransaction(CmpeUtil.getStringFromKey(keyPair.getPrivate()));

        Boolean response = cmpETransaction.isTransactionValid();

        assertThat(response).isTrue();
    }

    @Test
    void isTransactionInvalid() throws NoSuchAlgorithmException {

        SecureRandom secureRandom = new SecureRandom();
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048, secureRandom);
        KeyPair keyPair = keyPairGenerator.generateKeyPair();
        KeyPair keyPair2 = keyPairGenerator.generateKeyPair();

        CmpETransaction cmpETransaction = CmpETransaction.builder()
                .fromAddress(CmpeUtil.getStringFromKey(keyPair2.getPublic()))
                .amount(5L)
                .timestamp(4L)
                .toAddress("toAddress")
                .build();

        cmpETransaction.signTransaction(CmpeUtil.getStringFromKey(keyPair.getPrivate()));

        Boolean response = cmpETransaction.isTransactionValid();

        assertThat(response).isFalse();
    }

}