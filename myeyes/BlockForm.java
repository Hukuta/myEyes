package myeyes;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.Timer;

/**
 *
 * @author developer
 */
public class BlockForm extends javax.swing.JFrame {

    private Timer t;

    /**
     * Creates new form BlockForm
     */
    public BlockForm() {

        initComponents();

        java.awt.Dimension screenSize = java.awt.Toolkit.getDefaultToolkit().getScreenSize();
        int border = 10;
        setLocation(0, border);
        screenSize.height -= border * 2;

        javax.swing.JPanel jPanel0 = new javax.swing.JPanel();
        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel0);
        jPanel0.setBackground(Color.BLACK);
        jPanel0.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGap(0, screenSize.width, Short.MAX_VALUE));
        jPanel1Layout.setVerticalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGap(0, 30, Short.MAX_VALUE));
        getContentPane().add(jPanel0);

        javax.swing.JLabel textWaitTime = new javax.swing.JLabel();
        textWaitTime.setFont(new java.awt.Font("Arial", 0, 16));
        textWaitTime.setForeground(java.awt.Color.LIGHT_GRAY);
        textWaitTime.setText("          Break ends at "
                + MyEyes.curTime(0L + MyEyes.breakTime));
        getContentPane().add(textWaitTime);

        javax.swing.JPanel jPanel1 = new javax.swing.JPanel();
        jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setBackground(Color.BLACK);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGap(0, screenSize.width, Short.MAX_VALUE));
        jPanel1Layout.setVerticalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGap(0, ((int) screenSize.height / 2) -46, Short.MAX_VALUE));

        getContentPane().add(jPanel1);


        javax.swing.JLabel text = new javax.swing.JLabel();
        text.setFont(new java.awt.Font("Arial", 0, 36)); // NOI18N
        text.setForeground(java.awt.Color.gray);
        text.setText("               Take a break!       ");
        getContentPane().add(text);

        javax.swing.JButton aButton = new javax.swing.JButton();

        aButton.setText("More " + timeF(MyEyes.interval2));
        aButton.setAlignmentX(1.0F);
        aButton.setAlignmentY(1.5F);
        aButton.setAutoscrolls(true);
        aButton.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        aButton.setMargin(new java.awt.Insets(10, 10, 10, 10));
        aButton.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseReleased(java.awt.event.MouseEvent evt) {
                MyEyes.aside();
                BlockForm.this.back2work();
            }
        });
        getContentPane().add(aButton);

        javax.swing.JLabel text2 = new javax.swing.JLabel();
        text2.setBackground(new java.awt.Color(0, 0, 0));
        text2.setFont(new java.awt.Font("Arial", 0, 16));
        text2.setForeground(java.awt.Color.gray);
        text2.setText("                                                  or  ");
        //text2.setLayout(this.getLayout());
        getContentPane().add(text2);

        javax.swing.JButton close2workButton = new javax.swing.JButton();
        close2workButton.setText("More " + timeF(MyEyes.interval));
        close2workButton.setAlignmentX(1.0F);    
        close2workButton.setAlignmentY(1.5F);
        close2workButton.setAutoscrolls(true);
        close2workButton.setHorizontalTextPosition(javax.swing.SwingConstants.RIGHT);
        close2workButton.setMargin(new java.awt.Insets(1, 1, 1, 1));
        close2workButton.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseReleased(java.awt.event.MouseEvent evt) {
                MyEyes.asideLong();
                BlockForm.this.back2work();
            }
        });
        getContentPane().add(close2workButton);
        
        setPreferredSize(screenSize);
        setSize(screenSize);

        getContentPane().setBackground(Color.BLACK);

        ActionListener taskPerformer = new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                if (MyEyes.working == true) {
                    BlockForm.this.back2work();
                }
            }
        };
        t = new Timer(1000, taskPerformer);
        t.start();
    }

    public void back2work() {

        if (t != null) {
            t.stop();
            t = null;
        }
        //exit window
        dispose();
        
    }

    public String timeF(Integer longTime) {
        float minuts = 0, seconds = longTime;
        minuts = (int) (longTime / 60);
        seconds -= minuts * 60;        
        if (minuts > 0) {
            if (seconds > 0) {                
                return (int) minuts + " min " + (int)seconds + " sec";
            } else {
                return (int) minuts + " min";
            }
        } else {
            return (int)seconds + " sec";
        }
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
        setTitle("Take a break!"); // NOI18N
        setAlwaysOnTop(true);
        setBackground(java.awt.Color.black);
        setCursor(new java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR));
        setFocusable(false);
        setUndecorated(true);
        setPreferredSize(new java.awt.Dimension(600, 800));
        setResizable(false);
        setType(java.awt.Window.Type.POPUP);
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                formMouseEntered(evt);
            }
        });
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowOpened(java.awt.event.WindowEvent evt) {
                opened(evt);
            }
        });
        getContentPane().setLayout(new java.awt.FlowLayout());

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void formMouseEntered(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseEntered
        try {
            com.sun.awt.AWTUtilities.setWindowOpacity(this, 0.5f);
        } catch (java.lang.UnsupportedOperationException ue) {
            //System.out.println("Unsupported Operation: setWindowOpacity\n");
        }
        this.setBackground(Color.BLACK);
    }//GEN-LAST:event_formMouseEntered

    private void opened(java.awt.event.WindowEvent evt) {//GEN-FIRST:event_opened
    }//GEN-LAST:event_opened
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}
