package model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import service.CmpeUtil;

import java.security.MessageDigest;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;


@Data
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class CmpETransaction {
    private Long timestamp;
    private Long amount;
    private String fromAddress;
    private String toAddress;
    private byte[] signature;


    String calculateTransactionHash() {
        String data=fromAddress+'/'+toAddress+'/'+amount+'/'+timestamp;
        return CmpeUtil.hash(data);
    }

    public void signTransaction(String secretKey) {
        String data = fromAddress+'/'+toAddress+'/'+amount+'/'+timestamp;
        Signature transact;
        byte[] finalSignature;
        try {
            transact = Signature.getInstance("SHA256withRSA");
            transact.initSign(CmpeUtil.getPrivateKeyFromString(secretKey));
            transact.update(data.getBytes());
            finalSignature = transact.sign();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        signature = finalSignature;
    }

    public Boolean isTransactionValid() {
        String data = fromAddress+'/'+toAddress+'/'+amount+'/'+timestamp;
        try {
            Signature ecdsaVerify = Signature.getInstance("SHA256withRSA");
            ecdsaVerify.initVerify(CmpeUtil.getPublicKeyFromString(fromAddress));
            ecdsaVerify.update(data.getBytes());
            return ecdsaVerify.verify(signature);
        }catch(Exception e) {
            throw new RuntimeException(e);
        }
    }



}
