package src;

import java.util.HashMap;
import java.util.Map;

import javax.swing.*;
import java.awt.CardLayout;
import java.awt.Font;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Insets;

/**
 * @author Randolph, Liyuan
 */
public class LoginGUI {
	private JFrame frame;
	
	private JPanel panelLogin;
	private JPanel panelRegister;
    private JPanel resetPanel;

    private static final String FONT = "Tahoma";

	public static void main(String[] args) {
		LoginGUI newGUI = new LoginGUI();
	}
	
	/**
	 * Create the application
	 */
	public LoginGUI() {
		initialize();
	}
	
	/**
	 * Initialize the contents of the frame and three panels
	 */
	private void initialize() {
		initializeframe();

        initializePanelLogin();
        initializePanelRegister();
        initializePanelReset();
        
        frame.setVisible(true);
    }

    /**
     * Initialize the contents of the frame
     */
    private void initializeframe(){
		frame = new JFrame();
		frame.setResizable(false);
		frame.setTitle("Bill Splitting System");
		frame.getContentPane().setEnabled(false);
        frame.setSize(600, 345);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.getContentPane().setLayout(new CardLayout(0, 0));
    }

    /**
     * Initialize the contents of the login
     */
    private void initializePanelLogin(){
        panelLogin = new JPanel();
        frame.getContentPane().add(panelLogin);
        GridBagLayout gblPanelLogin = new GridBagLayout();
        gblPanelLogin.columnWidths = new int[] {30, 160, 30, 200, 30};
        gblPanelLogin.rowHeights = new int[] {30, 30, 30, 30, 0, 0, 0, 0, 0, 0, 30, 30};
        gblPanelLogin.columnWeights = new double[]{0.0, 0.0, 0.0, 0.0};
        gblPanelLogin.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        panelLogin.setLayout(gblPanelLogin);
        
        JLabel titleLabel = new JLabel("Bill Splitting System");
        titleLabel.setFont(new Font("Viner Hand ITC", Font.BOLD, 30));
        GridBagConstraints gbcTitleLabel = new GridBagConstraints();
        gbcTitleLabel.gridheight = 3;
        gbcTitleLabel.gridwidth = 5;
        gbcTitleLabel.insets = new Insets(0, 0, 5, 0);
        gbcTitleLabel.gridx = 0;
        gbcTitleLabel.gridy = 1;
        panelLogin.add(titleLabel, gbcTitleLabel);
        
        JLabel userLabel = new JLabel("UserName/ Phone Number/ Account ID");
        userLabel.setFont(new Font(FONT, Font.PLAIN, 16));
        GridBagConstraints gbcUserLabel = new GridBagConstraints();
        gbcUserLabel.fill = GridBagConstraints.BOTH;
        gbcUserLabel.insets = new Insets(0, 0, 5, 5);
        gbcUserLabel.gridx = 1;
        gbcUserLabel.gridy = 4;
        panelLogin.add(userLabel, gbcUserLabel);
        
        JTextField userText = new JTextField();
        GridBagConstraints gbcUserText = new GridBagConstraints();
        gbcUserText.fill = GridBagConstraints.BOTH;
        gbcUserText.insets = new Insets(0, 0, 5, 5);
        gbcUserText.gridx = 3;
        gbcUserText.gridy = 4;
        panelLogin.add(userText, gbcUserText);
        userText.setColumns(10);
        
        JLabel passwordLabel = new JLabel("Password");
        passwordLabel.setFont(new Font(FONT, Font.PLAIN, 16));
        GridBagConstraints gbcPasswordLabel = new GridBagConstraints();
        gbcPasswordLabel.fill = GridBagConstraints.BOTH;
        gbcPasswordLabel.insets = new Insets(0, 0, 5, 5);
        gbcPasswordLabel.gridx = 1;
        gbcPasswordLabel.gridy = 5;
        panelLogin.add(passwordLabel, gbcPasswordLabel);
        
        JPasswordField passwordText = new JPasswordField();
        GridBagConstraints gbcPasswordText = new GridBagConstraints();
        gbcPasswordText.fill = GridBagConstraints.BOTH;
        gbcPasswordText.insets = new Insets(0, 0, 5, 5);
        gbcPasswordText.gridx = 3;
        gbcPasswordText.gridy = 5;
        panelLogin.add(passwordText, gbcPasswordText);
        
        JButton loginButton = new JButton("Login");
        loginButton.addActionListener(arg0 -> {
            // if missing input
            if (userText.getText() == null || passwordText == null) {
                JOptionPane.showMessageDialog(frame, "Missing login info...");
                return;
            }

            Map<String, String> loginInfo = new HashMap<>();
            loginInfo.put(SchemaFields.USERNAME, userText.getText());
            loginInfo.put(SchemaFields.PASSWORD, new String(passwordText.getPassword()));

            Users u1 = new Users();
            // if login failed
            if (!u1.instantiateUser(loginInfo)) {
                JOptionPane.showMessageDialog(frame, "UserName and password does not match. Please try again...");
                return;
            }

            // if userName and password are matched in the database
            // then enter the main menu GUI
            frame.setVisible(false);

            MainPageGUI mainPage = new MainPageGUI(u1);
        });
        
        loginButton.setFont(new Font("Yu Gothic", Font.BOLD, 24));
        GridBagConstraints gbcLoginButton = new GridBagConstraints();
        gbcLoginButton.gridheight = 2;
        gbcLoginButton.gridwidth = 5;
        gbcLoginButton.insets = new Insets(0, 0, 5, 0);
        gbcLoginButton.gridx = 0;
        gbcLoginButton.gridy = 7;
        panelLogin.add(loginButton, gbcLoginButton);
        
        JButton signUpButton = new JButton("Sign Up");
        signUpButton.addActionListener(e -> {
            panelLogin.setVisible(false);
            panelRegister.setVisible(true);
        });
        GridBagConstraints gbcSignUpButton = new GridBagConstraints();
        gbcSignUpButton.anchor = GridBagConstraints.WEST;
        gbcSignUpButton.gridheight = 2;
        gbcSignUpButton.gridwidth = 2;
        gbcSignUpButton.insets = new Insets(0, 0, 5, 5);
        gbcSignUpButton.gridx = 0;
        gbcSignUpButton.gridy = 9;
        panelLogin.add(signUpButton, gbcSignUpButton);
        
        JButton forgetPasswordButton = new JButton("Forget Password");
        forgetPasswordButton.addActionListener(e -> {
            // enter the reset password GUI
            panelLogin.setVisible(false);
            resetPanel.setVisible(true);
        });
        GridBagConstraints gbcForgetPasswordButton = new GridBagConstraints();
        gbcForgetPasswordButton.insets = new Insets(0, 0, 5, 0);
        gbcForgetPasswordButton.gridwidth = 3;
        gbcForgetPasswordButton.gridheight = 2;
        gbcForgetPasswordButton.anchor = GridBagConstraints.EAST;
        gbcForgetPasswordButton.gridx = 2;
        gbcForgetPasswordButton.gridy = 9;
        panelLogin.add(forgetPasswordButton, gbcForgetPasswordButton);
    }

    /**
     * Initialize the contents of the register
     */
    private void initializePanelRegister(){
        panelRegister = new JPanel();
        frame.getContentPane().add(panelRegister);

        JButton backButton = new JButton("Back");
        backButton.addActionListener(e -> {
            // return to login page GUI
            panelRegister.setVisible(false);
            panelLogin.setVisible(true);
        });
        panelRegister.setLayout(null);
        backButton.setFont(new Font(FONT, Font.PLAIN, 16));
        backButton.setBounds(40, 49, 90, 39);
        panelRegister.add(backButton);

        JLabel nameLabel = new JLabel("UserName*");
        nameLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        nameLabel.setBounds(40, 183, 200, 22);
        nameLabel.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(nameLabel);

        JTextField nameText = new JTextField();
        nameText.setBounds(294, 185, 195, 22);
        panelRegister.add(nameText);

        JLabel phoneNumLabel = new JLabel("Phone Number*");
        phoneNumLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        phoneNumLabel.setBounds(40, 214, 200, 25);
        phoneNumLabel.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(phoneNumLabel);

        JTextField phoneNumText = new JTextField();
        phoneNumText.setBounds(294, 215, 195, 22);
        panelRegister.add(phoneNumText);

        JLabel emailabel = new JLabel("Email*");
        emailabel.setHorizontalAlignment(SwingConstants.RIGHT);
        emailabel.setBounds(40, 244, 200, 25);
        emailabel.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(emailabel);

        JTextField emailText = new JTextField();
        emailText.setBounds(294, 245, 195, 22);
        panelRegister.add(emailText);

        JLabel newPasswordLabel = new JLabel("Password*");
        newPasswordLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        newPasswordLabel.setBounds(40, 274, 200, 25);
        newPasswordLabel.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(newPasswordLabel);

        JPasswordField newPasswordText = new JPasswordField();
        newPasswordText.setBounds(294, 275, 195, 22);
        panelRegister.add(newPasswordText);

        JLabel rePasswordLabel = new JLabel("Type Password Again*");
        rePasswordLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        rePasswordLabel.setBounds(40, 304, 200, 25);
        rePasswordLabel.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(rePasswordLabel);

        JPasswordField rePasswordText = new JPasswordField();
        rePasswordText.setBounds(294, 305, 195, 22);
        panelRegister.add(rePasswordText);

        JButton registerButton = new JButton("    Register    ");
        registerButton.setBounds(204, 398, 190, 49);
        registerButton.addActionListener(e -> {
            // if there is missing input
            if (nameText.getText() == null || phoneNumText.getText() == null || emailText.getText() == null
                    || newPasswordText.getText() == null || rePasswordText.getText() == null) {
                JOptionPane.showMessageDialog(frame, "Missing register info...");
                return;
            }

            // if two password is not equal
            if (!newPasswordText.getText().equals(rePasswordText.getText())) {
                JOptionPane.showMessageDialog(frame, "Two password are not the same...");
                return;
            }

            Map<String, String> newUserInfo = new HashMap<>();
            newUserInfo.put(SchemaFields.USERNAME, nameText.getText());
            newUserInfo.put(SchemaFields.PHONE, phoneNumText.getText());
            newUserInfo.put(SchemaFields.EMAIL, emailText.getText());
            newUserInfo.put(SchemaFields.PASSWORD, new String(newPasswordText.getPassword()));
            newUserInfo.put(SchemaFields.NICKNAME, nameText.getText());

            Users u1 = new Users();

            // if register failed
            if (!u1.createAccount(newUserInfo)) {
                JOptionPane.showMessageDialog(frame, "Register failed. Please try again...");
                return;
            }

            // if all check processes are passed and succeed in registering new account
            panelRegister.setVisible(false);
            panelLogin.setVisible(true);
        });
        

        JLabel passwordHint = new JLabel("**Password should be at least 8-digit.");
        passwordHint.setBounds(120, 335, 520, 25);
        passwordHint.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(passwordHint);
        JLabel passwordHint2 = new JLabel("**Other should be non-empty.");
        passwordHint2.setBounds(120, 360, 520, 25);
        passwordHint2.setFont(new Font(FONT, Font.PLAIN, 18));
        panelRegister.add(passwordHint2);

        registerButton.setFont(new Font("Yu Gothic", Font.BOLD, 24));
        panelRegister.add(registerButton);
    }

    /**
     * Initialize the contents of the reset
     */
    private void initializePanelReset() {
        resetPanel = new JPanel();
        frame.setSize(600, 600);
        frame.getContentPane().add(resetPanel);
        resetPanel.setLayout(null);

        JLabel resetTitle = new JLabel("Reset Password");
        resetTitle.setHorizontalAlignment(SwingConstants.CENTER);
        resetTitle.setFont(new Font(FONT, Font.PLAIN, 22));
        resetTitle.setBounds(154, 61, 256, 53);
        resetPanel.add(resetTitle);

        JLabel emailLabel = new JLabel("Enter your username:");
        emailLabel.setHorizontalAlignment(SwingConstants.CENTER);
        emailLabel.setFont(new Font(FONT, Font.PLAIN, 16));
        emailLabel.setBounds(60, 169, 200, 30);
        resetPanel.add(emailLabel);

        JTextField emailField = new JTextField();
        emailField.setBounds(290, 170, 220, 30);
        resetPanel.add(emailField);
        emailField.setColumns(10);

        JLabel codeLabel = new JLabel("Enter the verification code:");
        codeLabel.setHorizontalAlignment(SwingConstants.CENTER);
        codeLabel.setFont(new Font(FONT, Font.PLAIN, 16));
        codeLabel.setBounds(60, 297, 200, 30);
        resetPanel.add(codeLabel);

        JTextField codeField = new JTextField();
        codeField.setColumns(10);
        codeField.setBounds(290, 298, 220, 30);
        resetPanel.add(codeField);

        JButton checkButton = new JButton("Send Verification code");
        checkButton.addActionListener(e -> {
            Users u1 = new Users();
            Map<String, String> sendInfo = new HashMap<>();
            sendInfo.put(SchemaFields.USERNAME, emailField.getText());
            sendInfo.put(SchemaFields.PASSWORD, "");
            sendInfo.put(SchemaFields.CODE, "");
            if (u1.resetPassword(sendInfo)) {
                JOptionPane.showMessageDialog(frame, "Verification code has been sent...");
            } else {
                JOptionPane.showMessageDialog(frame, "Sending verification code failed...");
            }
        });
        checkButton.setFont(new Font(FONT, Font.PLAIN, 16));
        checkButton.setBounds(180, 232, 200, 30);
        resetPanel.add(checkButton);

        JButton backButton = new JButton("Back");
        backButton.addActionListener(e -> {
            resetPanel.setVisible(false);
            panelLogin.setVisible(true);
        });
        backButton.setFont(new Font(FONT, Font.PLAIN, 16));
        backButton.setBounds(12, 24, 86, 36);
        resetPanel.add(backButton);

        JLabel password1Label = new JLabel("Enter your new password:");
        password1Label.setHorizontalAlignment(SwingConstants.CENTER);
        password1Label.setFont(new Font(FONT, Font.PLAIN, 16));
        password1Label.setBounds(60, 340, 200, 30);
        resetPanel.add(password1Label);

        JLabel password2Label = new JLabel("Repeat your new password:");
        password2Label.setHorizontalAlignment(SwingConstants.CENTER);
        password2Label.setFont(new Font(FONT, Font.PLAIN, 16));
        password2Label.setBounds(60, 383, 200, 30);
        resetPanel.add(password2Label);

        JPasswordField password1Field = new JPasswordField();
        password1Field.setBounds(290, 341, 220, 30);
        resetPanel.add(password1Field);

        JPasswordField password2Field = new JPasswordField();
        password2Field.setBounds(290, 384, 220, 30);
        resetPanel.add(password2Field);

        JButton resetButton = new JButton("Reset Password");
        resetButton.addActionListener(e -> {
            if (!password1Field.getText().equals(password2Field.getText())) {
                JOptionPane.showMessageDialog(frame, "Two password is not equal...");
                return;
            }
            Users u1 = new Users();
            Map<String, String> sendInfo = new HashMap<>();
            sendInfo.put(SchemaFields.USERNAME, emailField.getText());
            sendInfo.put(SchemaFields.PASSWORD, password1Field.getText());
            sendInfo.put(SchemaFields.CODE, codeField.getText());
            if (u1.resetPassword(sendInfo)) {
                JOptionPane.showMessageDialog(frame, "Password has been changed...");
                resetPanel.setVisible(false);
                panelLogin.setVisible(true);
            } else {
                JOptionPane.showMessageDialog(frame, "Resetting password failed...");
            }
        });
        resetButton.setFont(new Font(FONT, Font.PLAIN, 16));
        resetButton.setBounds(180, 442, 200, 43);
        resetPanel.add(resetButton);
    }
}

