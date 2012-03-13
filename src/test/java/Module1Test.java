import static org.testng.AssertJUnit.*;
import org.testng.annotations.Test;
import org.testng.annotations.Listeners;

@Listeners({ Listener.class })
public class Module1Test {
	@Test(description = "this is test1 description"
			, enabled = true			
			, timeOut = 30 * 1000
			, groups = { "P0", "BVT" })
	public void TC00001() {
		assertEquals(1, 1);
	}

	@Test(description = "this is test2 update description"
			, enabled = true			
			, timeOut = 30 * 1000
			, groups = { "P1", "FVT" })
	public void TC00002() {
		assertEquals(1, 1);
	}
	
	@Test(description = "this is test3 description"
			, enabled = true			
			, timeOut = 30 * 1000
			, groups = { "P2", "BVT" })
	public void TC00003() {
		assertEquals(1, 1);
	}
}
