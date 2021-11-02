package model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import service.CmpeUtil;

import java.util.List;
import java.util.Random;
import java.util.stream.IntStream;


@Data
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class CmpEBlock {
    public String prevBlockHash; 
    private String currBlockHash;
    private Long timestamp;
    private List<CmpETransaction> transactions;
    private Long proofOfWork;
    private static int difficulty = 1;

    public String calculateCurrBlockHash(){
        String data=prevBlockHash;
        for (CmpETransaction transaction : transactions) {
            data = data.concat(transaction.calculateTransactionHash());
        }
        data=data.concat(Long.toString(proofOfWork));
        data=data.concat(Long.toString(timestamp));
        return this.currBlockHash = CmpeUtil.hash(data);
    }

    public void validateBlock(){
        this.timestamp=System.currentTimeMillis();

        //Mining block
        Random rand = new Random();
        this.proofOfWork = rand.nextLong();
        while(difficulty>calculateZeros(calculateCurrBlockHash())) {
            this.proofOfWork= rand.nextLong();
        }

        //Validate
        calculateCurrBlockHash();
        difficulty++;
    }

    public boolean hasValidTransactions(){
        return IntStream.range(0, transactions.size()).allMatch(i -> transactions.get(i).isTransactionValid());
    }

    //Count 0's in the head of string
    private int calculateZeros(String myString){
        for(int i=0;i<myString.length();i++){
            if(myString.charAt(i)!='0'){
                return i;
            }
        }
        return -1;
    }

    private static void setDifficulty(int d){
        difficulty = d;
    }
}
