package model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import service.WalletService;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Data
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class CmpEBlockchain {
    private List<CmpEBlock> chain;
    private List<CmpETransaction> pendingTransactions;
    private Long difficulty;
    private static final Long validationReward = 100L;

    public void createInitialDummyBlock(){
        //create first dummy block, previos hash is 0
        List<CmpETransaction> transactions=new ArrayList<>();
        CmpEBlock firstBlock= CmpEBlock.builder().prevBlockHash("0").transactions(transactions).build();
        chain = new ArrayList();
        chain.add(firstBlock);
    }

    // Loops over all the blocks in
    // the chain and verify if they are properly linked
    // together and nobody has tampered with the
    // hashes.
    private Boolean isChainValid(){
        CmpEBlock currentBlock;
        CmpEBlock previousBlock;

        for (int i = 1;
             i < chain.size();
             i++) {

            currentBlock = chain.get(i);
            previousBlock = chain.get(i - 1);

            if (!currentBlock.getCurrBlockHash().equals(currentBlock.calculateCurrBlockHash())||
                    !previousBlock.getCurrBlockHash().equals(currentBlock.prevBlockHash)) {

                return false;
            }
        }
        return true;
    }

    // If transaction is not valid, no operation
    private void addTransactionToPendingList(CmpETransaction transx){
        if(transx.isTransactionValid()){
            pendingTransactions.add(transx);
        }
    }

    private void validatePendingTransactions(String rewardAddress){
        // Create reward transaction
        CmpETransaction rewardTransaction = CmpETransaction.builder()
                .toAddress(rewardAddress)
                .timestamp(System.currentTimeMillis())
                .amount(validationReward)
                .build();

        // Reward transaction needs to be signed
        rewardTransaction.signTransaction(rewardAddress);

        CmpEBlock block;
        synchronized (pendingTransactions){
            CmpEBlock lastBlock = chain.get(chain.size()-1);
            block = CmpEBlock.builder()
                    .prevBlockHash(lastBlock.getCurrBlockHash())
                    .timestamp(System.currentTimeMillis())
                    .transactions(pendingTransactions)
                    .build();  // Corresponding constructor has to call POW calculation and Current Block Hash from these values
            pendingTransactions = new ArrayList<>(); // Clear pending transactions now
        }
        System.out.println("Block validation operation ?? " + block.toString());
    }

    Long getBalanceOf(String address){
        return getAllTransactionsFor(address).stream()
                .mapToLong( it ->
                (it.getFromAddress().equals(address) ? -1 : 1) * it.getAmount())
                .sum();
    }

    private List<CmpETransaction> getAllTransactionsFor(String address){
        return chain.stream().map(CmpEBlock::getTransactions).flatMap(Collection::stream)
                .filter(it -> it.getFromAddress().equals(address) || it.getToAddress().equals(address))
                .collect(Collectors.toList());
    }
}
