package edu.cwru.csds393.billsplit;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {BillsplitBackendApplication.class})
@Import(BillSplitTestConfiguration.class)
class BillsplitBackendApplicationTests {
    @Test
    void contextLoads() {
    }

}
