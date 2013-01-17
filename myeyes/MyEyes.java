
package myeyes;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.Timer;


/**
 * Small program for make breaks
 *
 * @author developer
 */
public class MyEyes {
    // Interval between breaks
    public static Integer interval = 3000; //50 min
    // breaks time
    protected static Integer breakTime = 240; //4 min
    // interval if asided
    public static Integer interval2 = 180; //3 min

    // Time passed
    protected static Long tp = new Long(0);
    // First state is working
    public static Boolean working = true;
    // is asided
    protected static Boolean asided = false;
    //timer interval
    protected static int timerInterval = 10;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        if(args.length == 1 && args[0].equals("test")) {
            //debug values
            interval = 10;
            breakTime = 5;
            interval2 = 5;
            timerInterval = 1;
        }
        
        ActionListener taskPerformer = new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent evt) {
                tp += timerInterval;

                if (working) {//Time to make a break ?
                    if (asided) {
                        if (tp >= interval2) {
                            asided = false;
                            relax();
                        }
                    } else {
                        if (tp >= interval) {
                            relax();
                        }
                    }
                } else if (tp >= breakTime) {
                    //Time to work
                    working = true;
                    tp = new Long(0);
                }
            }

            public void relax(){
                working = false;//stop working
                tp = new Long(0);//refresh timer

                java.awt.EventQueue.invokeLater(new Runnable() {
                    @Override
                    public void run() {
                        new BlockForm().setVisible(true);
                    }
                });
            }
        };

        Timer t = new Timer(timerInterval * 1000, taskPerformer);
        t.start();

        /*
        System.out.println("'q' to exit\n");
        int code;
        try {
            while (-1 != (code = System.in.read())) {
                if ('q' == (char) code) {
                    System.exit(0);
                }
            }
        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
        */
         
        while (true) {
            try {
                Thread.sleep((int) timerInterval / 2);
            } catch (InterruptedException ex) {
                System.out.println(ex.getMessage());
            }
        }
    }

    public static void aside() {
        asided = true;
        System.gc();
    }


}