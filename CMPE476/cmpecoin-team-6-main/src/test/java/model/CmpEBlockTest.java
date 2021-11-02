package model;

import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import service.CmpeUtil;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;


class CmpEBlockTest {

//    @Test
//    void calculateCurrBlockHashTEST() {
//        //given
//        final String prevBlockHash = "prevBlockHash";
//        final int difficulty=5;
//        CmpEBlock cmpEBlock = CmpEBlock.builder()
//                .prevBlockHash(prevBlockHash)
//                .transactions(List.of())
//                .build();
//        cmpEBlock.validateBlock(difficulty);
//
//        try (MockedStatic<CmpeUtil> mocked = mockStatic(CmpeUtil.class)) {
//            // Mocking
//            final String data = prevBlockHash.concat(Long.toString(cmpEBlock.getProofOfWork())).concat(Long.toString(cmpEBlock.getTimestamp()));
//            mocked.when(() -> CmpeUtil.hash(data)).thenReturn("HASH");
//
//            //When
//            cmpEBlock.calculateCurrBlockHash();
//
//            // Verifying mocks.
//            mocked.verify(times(1), () -> CmpeUtil.hash(data));
//        }
//
//        //then
//        assertThat(cmpEBlock.getCurrBlockHash()).isNotEmpty();
//        assertThat(cmpEBlock.getCurrBlockHash()).isEqualTo("HASH");
//    }
//
//    @Test
//    void calculateCurrBlockHashWithTransactionsTEST() {
//        //given
//        CmpETransaction transaction1 = CmpETransaction.builder().build();
//        CmpETransaction transaction2 = CmpETransaction.builder().build();
//        CmpETransaction transaction3 = CmpETransaction.builder().build();
//
//        final String prevBlockHash = "prevBlockHash";
//        final int difficulty=5;
//        CmpEBlock cmpEBlock = CmpEBlock.builder()
//                .prevBlockHash(prevBlockHash)
//                .transactions(List.of(transaction1, transaction2, transaction3))
//                .build();
//        cmpEBlock.validateBlock(difficulty);
//
//        try (MockedStatic<CmpeUtil> mocked = mockStatic(CmpeUtil.class)) {
//            // Mocking
//            mocked.when(() -> CmpeUtil.hash(anyString())).thenReturn("HASH");
//
//            //When
//            cmpEBlock.calculateCurrBlockHash();
//
//            // Verifying mocks.
////           mocked.verify(times(4), () -> CmpeUtil.hash(anyString()));; // it calls it for each transaction
//        }
//
//        //then
//        assertThat(cmpEBlock.getCurrBlockHash()).isNotEmpty();
//        assertThat(cmpEBlock.getCurrBlockHash()).isEqualTo("HASH");
//        assertThat(cmpEBlock.getPrevBlockHash()).isEqualTo(prevBlockHash);
//    }
//
//
//    @Test
//    void validateBlockTEST() {
//        //given
//        int difficulty=5;
//        CmpEBlock cmpEBlock= CmpEBlock.builder().prevBlockHash("prev").transactions(List.of()).build();
//
//        //when
//        cmpEBlock.validateBlock(4);
//
//        //then
//        assertThat(cmpEBlock.getCurrBlockHash().substring(0,4)).isEqualTo("0000");
//    }

    @Test
    void hasValidTransactionsTrueTest() {
        //given
        CmpETransaction transaction1 = Mockito.mock(CmpETransaction.class);

        CmpEBlock cmpEBlock= CmpEBlock.builder()
                .prevBlockHash("prev")
                .transactions(List.of(transaction1))
                .build();

        //when
        when(transaction1.isTransactionValid()).thenReturn(Boolean.TRUE);
        Boolean response = cmpEBlock.hasValidTransactions();

        //then
        assertThat(response).isTrue();
        //TODO IMPLEMENT IT AFTER TRANSACTION TESTS
    }

    @Test
    void hasValidTransactionsFalseTest() {
        //given
        CmpETransaction transaction1 = Mockito.mock(CmpETransaction.class);

        CmpEBlock cmpEBlock= CmpEBlock.builder()
                .prevBlockHash("prev")
                .transactions(List.of(transaction1))
                .build();

        //when
        when(transaction1.isTransactionValid()).thenReturn(Boolean.FALSE);
        Boolean response = cmpEBlock.hasValidTransactions();

        //then
        assertThat(response).isFalse();
        //TODO IMPLEMENT IT AFTER TRANSACTION TESTS
    }

}