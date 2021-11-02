package service;

import lombok.SneakyThrows;

import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class CmpeUtil {
    public static String getStringFromKey(Key key) {
        return Base64.getEncoder().encodeToString(key.getEncoded());
    }

    @SneakyThrows
    public static PrivateKey getPrivateKeyFromString(String keyString) {
        KeyFactory kf = KeyFactory.getInstance("RSA");
        PKCS8EncodedKeySpec keySpecPKCS8 = new PKCS8EncodedKeySpec(Base64.getDecoder().decode(keyString));
        return kf.generatePrivate(keySpecPKCS8);
    }

    @SneakyThrows
    public static PublicKey getPublicKeyFromString(String keyString) {
        KeyFactory kf = KeyFactory.getInstance("RSA");
        X509EncodedKeySpec keySpecX509 = new X509EncodedKeySpec(Base64.getDecoder().decode(keyString));
        return kf.generatePublic(keySpecX509);
    }


    //Calculate sha256 hash
    public static String hash(String myString){
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedHash = digest.digest(myString.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(encodedHash);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return "Error";
    }

    //Taken from
    //https://www.baeldung.com/sha-256-hashing-java
    public static String bytesToHex(byte[] hash) {
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
