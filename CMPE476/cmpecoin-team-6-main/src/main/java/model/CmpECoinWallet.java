package model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import lombok.RequiredArgsConstructor;
import service.CmpeUtil;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

@Data
@Builder
public class CmpECoinWallet {

    private String publicKey;
    private String privateKey;
    private Long currentBalance;

    public void generateKeyPair() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");

            // Initialize KeyPairGenerator.
//            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            SecureRandom random = new SecureRandom();
            keyGen.initialize(2048, random);

            // Generate Key Pairs, a private key and a public key.
            KeyPair keyPair = keyGen.generateKeyPair();
            this.publicKey = CmpeUtil.getStringFromKey(keyPair.getPublic());
            this.privateKey = CmpeUtil.getStringFromKey(keyPair.getPrivate());

        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}



