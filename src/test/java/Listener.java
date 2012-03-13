
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.annotation.Annotation;


import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestNGListener;
import org.testng.ITestResult;

public class Listener implements ITestListener {

    FileWriter fWriter = null;
    BufferedWriter writer = null;
	
	public Listener() {
	}

	@SuppressWarnings("deprecation")
	public void onTestStart(ITestResult arg0) {
			
		System.out.println(String.format("---------- onTestStart %s(%s) ----------", arg0.getName(), arg0.getMethod().getDescription()));
		int index = 1;
		for (Object o : arg0.getParameters()) {
			System.out.println(String.format("the %dst parameter is %s", index++, o));
		}
		
		index = 1;
		Annotation[] annos = arg0.getMethod().getConstructorOrMethod().getMethod().getAnnotations();
	    for(Annotation a : annos) {
	    	System.out.println(String.format("the %dst annotation is %s", index++, a));
	    }
	    
	}


	public void onTestSuccess(ITestResult arg0) {
		System.out.println(String.format("---------- onTestSuccess %s(%s) ----------", arg0.getName(), arg0.getMethod().getDescription()));
	
        try {        	        	
			writer.append(String.format("%s,%s,true", arg0.getName(), arg0.getMethod().getDescription()));
	        writer.newLine();
        } catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
	}
	
	public void onTestFailure(ITestResult arg0) {
		System.out.println(String.format("---------- onTestFailure %s(%s) ----------", arg0.getName(), arg0.getMethod().getDescription()));

        try {        	        	
			writer.append(String.format("%s,%s,false", arg0.getName(), arg0.getMethod().getDescription()));
	        writer.newLine();
        } catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
	}

	public void onTestSkipped(ITestResult arg0) {
		System.out.println(String.format("---------- onTestSkipped %s(%s) ----------", arg0.getName(), arg0.getMethod().getDescription()));
	}	
	
	public void onTestFailedButWithinSuccessPercentage(ITestResult arg0) {
		System.out.println(String.format("---------- onTestFailedButWithinSuccessPercentage %s(%s) ----------", arg0.getName(), arg0.getMethod().getDescription()));
	}		

	
	public void onStart(ITestContext arg0) {
		System.out.println(String.format("onStart"));
		
	    File f1 = new File("tc.csv");
	    boolean success = f1.delete();
	    
        try {
			fWriter = new FileWriter("tc.csv");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	    writer = new BufferedWriter(fWriter);		
	}	
	
	public void onFinish(ITestContext arg0) {
		System.out.println(String.format("onFinish"));
		
        try {
			writer.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}	
}
