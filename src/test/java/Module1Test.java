import static org.testng.AssertJUnit.*;
import org.testng.annotations.Test;


public class Module1Test {
	@Test(groups = { "P1", "FVT" })
	public void testMethod1() {
		assertEquals(1, 1);
	}

	@Test(groups = { "P2", "BVT" })
	public void testMethod2() {
		assertEquals(1, 2);
	}
	
	@Test(groups = { "P1", "FVT" })
	public void testMethod3() {
		assertEquals(1, 1);
	}
}
