package model;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class Message {
    private MessageType type;
    private String content;
    private CmpETransaction transaction;
    private CmpEBlock block;
    private String simpleNodeAddress;
    private String validatorNodeAddress;
    private List<CmpETransaction> transactions;
    private List<String> joinedNodeAddresses;
    private CmpEBlockchain chain;
}
