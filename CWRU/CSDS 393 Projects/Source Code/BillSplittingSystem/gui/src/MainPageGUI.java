package src;

import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Font;
import java.time.LocalDate;
import java.util.*;
import java.awt.event.ItemEvent;
import javax.swing.*;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartFrame;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

/**
 * @author Randolph, Liyuan
 */
class MainPageGUI {
    private JFrame frame;

    private JPanel mainPanel;
    private JPanel activityControlPanel;
    private JPanel createBookPanel;
    private JPanel addMemberPanel;
    private JPanel addActivityPanel;
    private JPanel viewActivityPanel;
    private JPanel deleteActivityPanel;
    private JPanel viewActivitySpendingsPanel;

    private JComboBox<String> bookListComboBox;
    private JComboBox<String> memberListBox;
    private JTextField userNameText;
    JTextArea textArea;
    private JTextArea activityDetail;

    private Users user;
    private Book accountBook;
    private List<Book> books;

    private int bookIndex = 0;
    private int memberIndex = 0;
    private int memberIndex2 = 0;
    private int currencyIndex = 0;
    private int categoryIndex = 0;
    private int activityIndex = 0;
    private int yearIndex = 0;
    private int monthIndex = 0;
    private int dayIndex = 0;

    public final String[] currencyArr = new String[] { "*", "USD", "EUR", "CNY", "GBP" };
    public final Double[] currencyValueArr = new Double[] { 1.0, 0.8454, 6.675, 0.7646 };
    public static final String[] categoryArr = new String[] { "*", "entertainment", "shopping", "transportation", "other" };
    public final String[] yearArr = new String[] { "*", "2016", "2017", "2018", "2019", "2020" };
    public final String[] monthArr = new String[] { "*", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"};
    public final String[] dayArr = new String[] { "*", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
            "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
            "25", "26", "27", "28", "29", "30", "31" };
    private final String[] informationTitle = new String[] {"ActivityName: ", "activityDate: ", "activityCategory: ", "activityAmount: "};

    private static final String TITLE = "Bill Splitting System";
    private static final String BACKTITLE = "    Back    ";

    private static final String FONT1 = "Tahoma";
    private static final String FONT2 = "Yu Gothic";
    private static final String FONT3 = "Dialog";

    /**
     * Create the application
     */
    public MainPageGUI(Users user) {
        this.user = user;
        initialize();
    }

    /**
     * Initialize the contents of the frame and three panels
     */
    private void initialize() {
        initializeframe();

        initializeMainPanel();

        frame.setVisible(true);
    }

    /**
     * Initialize the contents of the frame
     */
    private void initializeframe() {
        frame = new JFrame();
        frame.setResizable(false);
        frame.setTitle(TITLE);
        frame.getContentPane().setEnabled(false);
        frame.setSize(600, 600);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.getContentPane().setLayout(new CardLayout(0, 0));
    }

    /**
     * Initialize the contents of main panel
     */
    private void initializeMainPanel() {
        mainPanel = new JPanel();
        frame.getContentPane().add(mainPanel);
        mainPanel.setLayout(null);

        if (Objects.isNull(user))
            System.exit(0);
        books = user.getBooks();
        String[] bookInfo = new String[books.size()+1];
        bookInfo[0] = "*";
        for (int i = 1; i < bookInfo.length; ++i) {
            bookInfo[i] = books.get(i-1).getName();
        }
        bookListComboBox = new JComboBox<>(bookInfo);
        bookListComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                bookIndex = bookListComboBox.getSelectedIndex();
            }
        });

        JButton viewAccountButton = new JButton("View the Book");
        viewAccountButton.addActionListener(e -> {
            if (bookIndex == 0) {
                JOptionPane.showMessageDialog(frame, "Please select a book!");
                return;
            }
            accountBook = user.getBookbyID(bookIndex-1);
            initializeActivityControlPanel();
            mainPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });
        JButton createAccountButton = new JButton("Create new Book");
        createAccountButton.addActionListener(e -> {
            initializeCreateBookPanel();
            mainPanel.setVisible(false);
            createBookPanel.setVisible(true);
        });
        JButton deleteAccount = new JButton("Delete the Book");
        deleteAccount.addActionListener(e -> {
            if (bookIndex != 0) {
                if (user.deleteBook(bookIndex-1)) {
                    JOptionPane.showMessageDialog(frame, "Successfully delete a book!");
                    bookListComboBox.removeItemAt(bookIndex);
                } else {
                    JOptionPane.showMessageDialog(frame, "Failed to delete a book!");
                }
            } else {
                JOptionPane.showMessageDialog(frame, "Please select a book!");
            }
        });

        JLabel titleLabel = new JLabel(TITLE);
        titleLabel.setBounds(123, 38, 348, 49);
        titleLabel.setFont(new Font("Viner Hand ITC", Font.BOLD, 30));
        mainPanel.add(titleLabel);

        JLabel accountLabel = new JLabel("Your Accounts:");
        accountLabel.setBounds(30, 160, 149, 25);
        accountLabel.setFont(new Font(FONT1, Font.BOLD, 18));
        mainPanel.add(accountLabel);

        bookListComboBox.setBounds(82, 230, 412, 29);
        mainPanel.add(bookListComboBox);

        viewAccountButton.setBounds(77, 295, 165, 30);
        viewAccountButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        mainPanel.add(viewAccountButton);

        createAccountButton.setBounds(183, 383, 215, 30);
        createAccountButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        mainPanel.add(createAccountButton);

        deleteAccount.setFont(new Font(FONT1, Font.PLAIN, 16));
        deleteAccount.setBounds(329, 295, 200, 30);
        mainPanel.add(deleteAccount);
    }

    /**
     * Initialize the contents of the activity panel
     */
    private void initializeActivityControlPanel() {
        activityControlPanel = new JPanel();
        frame.getContentPane().add(activityControlPanel);
        activityControlPanel.setLayout(null);

        String[] memberInfo = new String[accountBook.getMemberList().size()+1];
        memberInfo[0] = "*";
        int index = 1;
        for (String member : accountBook.getMemberList()) {
            memberInfo[index] = member;
            ++index;
        }
        memberListBox = new JComboBox<>(memberInfo);
        memberListBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                memberIndex = memberListBox.getSelectedIndex();
            }
        });

        JButton addMemberButton = new JButton("Add new Member");
        addMemberButton.addActionListener(arg0 -> {
            initializeAddMemberPanel();
            activityControlPanel.setVisible(false);
            addMemberPanel.setVisible(true);
        });
        JButton deleteMemberButton = new JButton("Delete the Member");
        deleteMemberButton.addActionListener(e -> {
            if (memberIndex != 0) {
                if (accountBook.deleteMember(memberIndex-1)) {
                    JOptionPane.showMessageDialog(frame, "Successfully delete a member!");
                    memberListBox.removeItemAt(memberIndex);
                    activityControlPanel.revalidate();
                } else {
                    JOptionPane.showMessageDialog(frame, "Failed to delete a member!");
                }
            } else {
                JOptionPane.showMessageDialog(frame, "Please select a member!");
            }
        });

        JButton addActivityButton = new JButton("Add new Activity");
        addActivityButton.addActionListener(arg0 -> {
            initializeAddActivityPanel();
            activityControlPanel.setVisible(false);
            addActivityPanel.setVisible(true);
        });
        JButton viewActivityButton = new JButton("View All Activities");
        viewActivityButton.addActionListener(arg0 -> {
            initializeViewActivityPanel();
            activityControlPanel.setVisible(false);
            viewActivityPanel.setVisible(true);
        });
        JButton deleteActivityButton = new JButton("Delete Activity");
        deleteActivityButton.addActionListener(arg0 -> {
            initializeDeleteActivityPanel();
            activityControlPanel.setVisible(false);
            deleteActivityPanel.setVisible(true);
        });

        JButton dailyActivityButton = new JButton("View Activity Spendings");
        dailyActivityButton.addActionListener(arg0 -> {
            initializeViewActivitySpendingsPanel();
            activityControlPanel.setVisible(false);
            viewActivitySpendingsPanel.setVisible(true);
        });

        JLabel titleLabel = new JLabel(TITLE);
        titleLabel.setBounds(123, 34, 348, 49);
        titleLabel.setFont(new Font("Viner Hand ITC", Font.BOLD, 30));
        activityControlPanel.add(titleLabel);

        JLabel groupLabel = new JLabel("Account Members:");
        groupLabel.setBounds(30, 107, 185, 25);
        groupLabel.setFont(new Font(FONT1, Font.BOLD, 18));
        activityControlPanel.add(groupLabel);

        memberListBox.setBounds(93, 160, 270, 29);
        activityControlPanel.add(memberListBox);

        deleteMemberButton.setBounds(386, 159, 175, 29);
        deleteMemberButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(deleteMemberButton);

        addMemberButton.setBounds(197, 220, 166, 29);
        addMemberButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(addMemberButton);

        JLabel activityLabel = new JLabel("Activities:");
        activityLabel.setBounds(30, 275, 119, 22);
        activityLabel.setFont(new Font(FONT1, Font.BOLD, 18));
        activityControlPanel.add(activityLabel);

        addActivityButton.setBounds(70, 335, 160, 29);
        addActivityButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(addActivityButton);

        viewActivityButton.setBounds(70, 395, 160, 29);
        viewActivityButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(viewActivityButton);

        deleteActivityButton.setBounds(70, 455, 160, 29);
        deleteActivityButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(deleteActivityButton);

        dailyActivityButton.setBounds(330, 335, 250, 29);
        dailyActivityButton.setFont(new Font(FONT1, Font.PLAIN, 16));
        activityControlPanel.add(dailyActivityButton);
    }

    JTextField bookNameText;

    /**
     * Initialize the create book panel
     */
    private void initializeCreateBookPanel() {
        createBookPanel = new JPanel();
        frame.getContentPane().add(createBookPanel);
        createBookPanel.setLayout(null);

        JLabel createLabel = new JLabel("Create New Account Book");
        createLabel.setFont(new Font("Tw Cen MT", Font.BOLD, 30));
        createLabel.setHorizontalAlignment(SwingConstants.CENTER);
        createLabel.setBounds(0, 82, 594, 48);
        createBookPanel.add(createLabel);

        JLabel nameLabel = new JLabel("Account Book Name:");
        nameLabel.setHorizontalAlignment(SwingConstants.CENTER);
        nameLabel.setFont(new Font(FONT1, Font.PLAIN, 16));
        nameLabel.setBounds(60, 209, 159, 30);
        createBookPanel.add(nameLabel);

        bookNameText = new JTextField();
        bookNameText.setBounds(255, 210, 246, 30);
        createBookPanel.add(bookNameText);
        bookNameText.setColumns(10);

        JButton createButton = new JButton("Create");
        createButton.addActionListener(arg0 -> {
            if (bookNameText.getText()==null || bookNameText.getText().trim()==null) {
                JOptionPane.showMessageDialog(frame, "Should write book name!");
                return;
            }
            if (user.createBook(bookNameText.getText())) {
                JOptionPane.showMessageDialog(frame, "Create successfully!");
                books = user.getBooks();
                String[] bookInfo = new String[books.size()+1];
                bookInfo[0] = "*";
                for (int i = 1; i < bookInfo.length; ++i) {
                    bookInfo[i] = books.get(i-1).getName();
                }
                bookListComboBox.addItem(books.get(books.size()-1).getName());
                mainPanel.revalidate();
            } else {
                JOptionPane.showMessageDialog(frame, "Create failed!");
            }
        });
        createButton.setFont(new Font(FONT1, Font.PLAIN, 18));
        createButton.setBounds(198, 329, 198, 48);
        createBookPanel.add(createButton);


        JButton backButton = new JButton(BACKTITLE);
        backButton.addActionListener(e -> {
            createBookPanel.setVisible(false);
            mainPanel.setVisible(true);
        });
        backButton.setFont(new Font(FONT2, Font.BOLD, 24));
        backButton.setBounds(200, 500, 200, 49);
        createBookPanel.add(backButton);
    }

    /**
     * Initialize the add member panel
     */
    private void initializeAddMemberPanel() {
        addMemberPanel = new JPanel();
        addMemberPanel.setLayout(null);
        frame.getContentPane().add(addMemberPanel);

        JLabel addMemberLabel = new JLabel("Add new Member");
        addMemberLabel.setHorizontalAlignment(SwingConstants.CENTER);
        addMemberLabel.setFont(new Font(FONT3, Font.BOLD, 30));
        addMemberLabel.setBounds(0, 103, 594, 64);
        addMemberPanel.add(addMemberLabel);

        JButton backButton = new JButton("Back");
        backButton.addActionListener(arg0 -> {
            addMemberPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });
        backButton.setFont(new Font(FONT2, Font.BOLD, 24));
        backButton.setBounds(12, 13, 100, 35);
        addMemberPanel.add(backButton);

        JButton addButton = new JButton("Add");
        addButton.addActionListener(arg0 -> {
            if (userNameText.getText() == null || userNameText.getText().trim() == null) {
                JOptionPane.showMessageDialog(frame, "Should write member username!");
                return;
            }
            if (accountBook.addMember(userNameText.getText())) {
                JOptionPane.showMessageDialog(frame, "Successfully add a member!");
                memberListBox.addItem(userNameText.getText());
                activityControlPanel.revalidate();
            } else {
                JOptionPane.showMessageDialog(frame, "Failed to add a member!");
            }
        });
        addButton.setFont(new Font(FONT2, Font.BOLD, 24));
        addButton.setBounds(219, 350, 156, 49);
        addMemberPanel.add(addButton);

        userNameText = new JTextField();
        userNameText.setBounds(280, 239, 200, 30);
        addMemberPanel.add(userNameText);
        userNameText.setColumns(10);

        JLabel lblNewLabel = new JLabel("userName:");
        lblNewLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        lblNewLabel.setFont(new Font(FONT1, Font.PLAIN, 16));
        lblNewLabel.setBounds(125, 238, 100, 30);
        addMemberPanel.add(lblNewLabel);
    }

    /**
     * Initialize the view activity spending panel
     */
    private void initializeViewActivitySpendingsPanel() {
        viewActivitySpendingsPanel = new JPanel();
        viewActivitySpendingsPanel.setLayout(null);
        frame.getContentPane().add(viewActivitySpendingsPanel);

        JComboBox<String> yearComboBox = new JComboBox<>(yearArr);
        yearComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                yearIndex = yearComboBox.getSelectedIndex();
            }
        });
        JComboBox<String> monthComboBox = new JComboBox<>(monthArr);
        monthComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                monthIndex = monthComboBox.getSelectedIndex();
            }
        });
        JComboBox<String> dayComboBox = new JComboBox<>(dayArr);
        dayComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                dayIndex = dayComboBox.getSelectedIndex();
            }
        });

        JButton backButton = new JButton(BACKTITLE);
        backButton.addActionListener(arg0 -> {
            viewActivitySpendingsPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });

        JButton showButton = new JButton("Show");
        showButton.addActionListener(arg0 -> {
            final String SPENDINGTITLE = "total category Spending";
            final String CATEGORY = "Category";

            if (yearIndex == 0) {
                JOptionPane.showMessageDialog(frame, "Please choose year!");
                return;
            }
            if (monthIndex == 0 && dayIndex != 0) {
                JOptionPane.showMessageDialog(frame, "Please choose month or not choose day!");
                return;
            }
            if (monthIndex == 0 && dayIndex == 0) {
                // Make the chart
                DefaultCategoryDataset mDataset = new DefaultCategoryDataset();
                double[] arr = new double[]{0,0,0,0};
                for (FinancialActivity activity : accountBook.getActivity()) {
                    if (Integer.parseInt(yearArr[yearIndex]) == Integer.parseInt(activity.getActivityDate().substring(0, 4))) {
                        for(int i = 1; i <= 12; ++i)
                            if(i == Integer.parseInt(activity.getActivityDate().substring(5, 7)))
                                arr[activity.getActivityCategoryId()-accountBook.getCategoryIndexDiff()] += activity.getActivityCost();
                    }
                }

                for (int i = 1; i < 5; ++i) {
                    mDataset.addValue(arr[i-1], SPENDINGTITLE, categoryArr[i]);
                }

                JFreeChart mChart = ChartFactory.createLineChart("View by Year", CATEGORY, "Cost", mDataset,
                        PlotOrientation.VERTICAL, true, true, false);

                CategoryPlot mPlot = (CategoryPlot) mChart.getPlot();
                mPlot.setBackgroundPaint(Color.LIGHT_GRAY);
                mPlot.setRangeGridlinePaint(Color.BLUE);
                mPlot.setOutlinePaint(Color.RED);

                ChartFrame mChartFrame = new ChartFrame("View by Year", mChart);
                mChartFrame.pack();
                mChartFrame.setVisible(true);
            } else if (monthIndex != 0 && dayIndex == 0) {
                // Make the chart
                DefaultCategoryDataset mDataset = new DefaultCategoryDataset();
                double[] arr = new double[]{0,0,0,0};
                for (FinancialActivity activity : accountBook.getActivity()) {
                    if (Integer.parseInt(yearArr[yearIndex]) == Integer.parseInt(activity.getActivityDate().substring(0, 4))
                            && Integer.parseInt(monthArr[monthIndex])  == Integer.parseInt(activity.getActivityDate().substring(5, 7))) {
                        for(int i = 1; i <= 31; ++i)
                            if(i == Integer.parseInt(activity.getActivityDate().substring(8)))
                                arr[activity.getActivityCategoryId()-accountBook.getCategoryIndexDiff()] += activity.getActivityCost();
                    }
                }

                for (int i = 1; i < 5; ++i) {
                    mDataset.addValue(arr[i-1], SPENDINGTITLE, categoryArr[i]);
                }

                JFreeChart mChart = ChartFactory.createLineChart("View by Month", CATEGORY, "Cost", mDataset,
                        PlotOrientation.VERTICAL, true, true, false);

                CategoryPlot mPlot = (CategoryPlot) mChart.getPlot();
                mPlot.setBackgroundPaint(Color.LIGHT_GRAY);
                mPlot.setRangeGridlinePaint(Color.BLUE);
                mPlot.setOutlinePaint(Color.RED);

                ChartFrame mChartFrame = new ChartFrame("View by Month", mChart);
                mChartFrame.pack();
                mChartFrame.setVisible(true);
            } else {
                // Make the chart
                DefaultCategoryDataset mDataset = new DefaultCategoryDataset();
                double[] arr = new double[]{0,0,0,0};
                for (FinancialActivity activity : accountBook.getActivity()) {
                    if (Integer.parseInt(yearArr[yearIndex]) == Integer.parseInt(activity.getActivityDate().substring(0, 4))
                            && Integer.parseInt(monthArr[monthIndex])  == Integer.parseInt(activity.getActivityDate().substring(5, 7))
                            && Integer.parseInt(dayArr[dayIndex])  == Integer.parseInt(activity.getActivityDate().substring(8))) {
                        arr[activity.getActivityCategoryId()-accountBook.getCategoryIndexDiff()] += activity.getActivityCost();
                    }
                }

                for (int i = 1; i < 5; ++i) {
                    mDataset.addValue(arr[i-1], SPENDINGTITLE, categoryArr[i]);
                }

                JFreeChart mChart = ChartFactory.createLineChart("View by Day", CATEGORY, "Cost", mDataset,
                        PlotOrientation.VERTICAL, true, true, false);

                CategoryPlot mPlot = (CategoryPlot) mChart.getPlot();
                mPlot.setBackgroundPaint(Color.LIGHT_GRAY);
                mPlot.setRangeGridlinePaint(Color.BLUE);
                mPlot.setOutlinePaint(Color.RED);

                ChartFrame mChartFrame = new ChartFrame("View by Day", mChart);
                mChartFrame.pack();
                mChartFrame.setVisible(true);
            }
        });

        JLabel viewLabel = new JLabel("View Activity Spendings");
        viewLabel.setHorizontalAlignment(SwingConstants.CENTER);
        viewLabel.setFont(new Font(FONT3, Font.BOLD, 30));
        viewLabel.setBounds(0, 61, 650, 32);
        viewActivitySpendingsPanel.add(viewLabel);

        backButton.setFont(new Font(FONT2, Font.BOLD, 24));
        backButton.setBounds(200, 468, 200, 49);
        viewActivitySpendingsPanel.add(backButton);

        showButton.setFont(new Font(FONT2, Font.BOLD, 24));
        showButton.setBounds(417, 243, 125, 39);
        viewActivitySpendingsPanel.add(showButton);

        yearComboBox.setBounds(75, 250, 100, 30);
        viewActivitySpendingsPanel.add(yearComboBox);

        monthComboBox.setBounds(200, 250, 75, 30);
        viewActivitySpendingsPanel.add(monthComboBox);

        dayComboBox.setBounds(307, 250, 75, 30);
        viewActivitySpendingsPanel.add(dayComboBox);

        JLabel lblNewLabel = new JLabel("* Choose month, year, and date to show daily activity spendings");
        lblNewLabel.setFont(new Font(FONT1, Font.PLAIN, 16));
        lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
        lblNewLabel.setBounds(0, 315, 594, 32);
        viewActivitySpendingsPanel.add(lblNewLabel);

        JLabel label = new JLabel("* Choose month and year to show monthly activity spendings");
        label.setHorizontalAlignment(SwingConstants.CENTER);
        label.setFont(new Font(FONT1, Font.PLAIN, 16));
        label.setBounds(0, 361, 594, 32);
        viewActivitySpendingsPanel.add(label);

        JLabel yearlyHint = new JLabel("* Choose only year to show yearly activity spendings");
        yearlyHint.setHorizontalAlignment(SwingConstants.CENTER);
        yearlyHint.setFont(new Font(FONT1, Font.PLAIN, 16));
        yearlyHint.setBounds(0, 410, 594, 32);
        viewActivitySpendingsPanel.add(yearlyHint);

        JLabel yearLabel = new JLabel("Year:");
        yearLabel.setHorizontalAlignment(SwingConstants.CENTER);
        yearLabel.setFont(new Font(FONT1, Font.BOLD, 16));
        yearLabel.setBounds(75, 205, 56, 32);
        viewActivitySpendingsPanel.add(yearLabel);

        JLabel monthLabel = new JLabel("Month:");
        monthLabel.setHorizontalAlignment(SwingConstants.CENTER);
        monthLabel.setFont(new Font(FONT1, Font.BOLD, 16));
        monthLabel.setBounds(199, 205, 69, 32);
        viewActivitySpendingsPanel.add(monthLabel);

        JLabel dateLabel = new JLabel("Date:");
        dateLabel.setHorizontalAlignment(SwingConstants.CENTER);
        dateLabel.setFont(new Font(FONT1, Font.BOLD, 16));
        dateLabel.setBounds(306, 205, 56, 32);
        viewActivitySpendingsPanel.add(dateLabel);
    }

    /**
     * Initialize the add activity panel
     */
    private void initializeAddActivityPanel() {
        addActivityPanel = new JPanel();
        frame.getContentPane().add(addActivityPanel);
        addActivityPanel.setLayout(null);

        JLabel addActivityLabel = new JLabel("Add Activity");
        addActivityLabel.setBounds(200, 61, 200, 32);
        addActivityLabel.setFont(new Font("STXinwei", Font.BOLD, 30));
        addActivityPanel.add(addActivityLabel);

        JLabel acitivityNameLabel = new JLabel("Activity Name:*");
        acitivityNameLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        acitivityNameLabel.setBounds(75, 161, 150, 22);
        acitivityNameLabel.setFont(new Font(FONT1, Font.PLAIN, 18));
        addActivityPanel.add(acitivityNameLabel);

        JTextField acitivityName = new JTextField();
        acitivityName.setBounds(300, 160, 200, 30);
        addActivityPanel.add(acitivityName);
        acitivityName.setColumns(10);

        JLabel activityDateLabel = new JLabel("Activity Date:*");
        activityDateLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        activityDateLabel.setBounds(75, 220, 150, 25);
        activityDateLabel.setFont(new Font(FONT1, Font.PLAIN, 18));
        addActivityPanel.add(activityDateLabel);

        JTextField activityDate = new JTextField();
        activityDate.setBounds(300, 220, 200, 30);
        activityDate.setColumns(10);
        addActivityPanel.add(activityDate);

        JLabel activityAmountLabel = new JLabel("Activity Amount:*");
        activityAmountLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        activityAmountLabel.setBounds(75, 280, 150, 25);
        activityAmountLabel.setFont(new Font(FONT1, Font.PLAIN, 18));
        addActivityPanel.add(activityAmountLabel);

        JTextField activityAmount = new JTextField();
        activityAmount.setBounds(350, 280, 150, 30);
        activityAmount.setColumns(10);
        addActivityPanel.add(activityAmount);

        JLabel activityCategoryLabel = new JLabel("Activity Category:*");
        activityCategoryLabel.setBounds(50, 340, 175, 20);
        activityCategoryLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        activityCategoryLabel.setFont(new Font(FONT1, Font.PLAIN, 18));
        addActivityPanel.add(activityCategoryLabel);

        String[] memberInfo = new String[accountBook.getMemberList().size()+1];
        memberInfo[0] = "*";
        int index = 1;
        for (String member : accountBook.getMemberList()) {
            memberInfo[index] = member;
            ++index;
        }
        JComboBox<String> participantsComboBox = new JComboBox<>(memberInfo);
        participantsComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                memberIndex2 = participantsComboBox.getSelectedIndex();
            }
        });
        participantsComboBox.setBounds(275, 400, 150, 30);
        addActivityPanel.add(participantsComboBox);

        StringBuilder memberListString = new StringBuilder();
        memberListString.append("Participants: "+ user.getName());

        List<String> participants = new ArrayList<>();

        JButton addParticipantButton = new JButton("add");
        addParticipantButton.addActionListener(e -> {
            if (memberIndex2==0) {
                JOptionPane.showMessageDialog(frame, memberListString.toString());
                return;
            }
            memberListString.append(", "+memberInfo[memberIndex2]);
            JOptionPane.showMessageDialog(frame, memberListString.toString());
            participants.add(memberInfo[memberIndex2]);
        });
        addParticipantButton.setFont(new Font(FONT1, Font.PLAIN, 18));
        addParticipantButton.setBounds(450, 400, 75, 30);
        addActivityPanel.add(addParticipantButton);

        JLabel participantsLabel = new JLabel("Participant:");
        participantsLabel.setBounds(75, 400, 150, 20);
        participantsLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        participantsLabel.setFont(new Font(FONT1, Font.PLAIN, 18));
        addActivityPanel.add(participantsLabel);

        JButton addButton = new JButton("    Add    ");
        addButton.setBounds(200, 500, 200, 40);
        addButton.addActionListener(e -> {
            FinancialActivity fa = new FinancialActivity();
            if (!fa.isCorrectFormat(acitivityName.getText(), activityDate.getText(), activityAmount.getText())) {
                JOptionPane.showMessageDialog(frame, "Wrong format!");
                return;
            }
            if (categoryIndex == 0 || currencyIndex == 0) {
                JOptionPane.showMessageDialog(frame, "Choose category and currency!");
                return;
            }
            double costInUSD = 0.0;
            costInUSD = Double.parseDouble(activityAmount.getText()) / currencyValueArr[currencyIndex-1];
            HashMap<String, Object> activity = new HashMap<>();
            activity.put(SchemaFields.AMOUNT, costInUSD);
            activity.put(SchemaFields.DESCRIPTION, acitivityName.getText());
            activity.put(SchemaFields.DATE, LocalDate.parse(activityDate.getText()).toEpochDay());
            activity.put(SchemaFields.CATEGORYID, categoryIndex-1+accountBook.getCategoryIndexDiff());
            activity.put(SchemaFields.AUTHOR, user.getName());
            activity.put(SchemaFields.PARTICIPANTS, participants);
            activity.put(SchemaFields.ACCT_BOOK_ID, accountBook.getID());
            if (accountBook.addActivity(activity)) {
                JOptionPane.showMessageDialog(frame, "Successfully add an activity!");
                initializeViewActivityPanel();
            } else {
                JOptionPane.showMessageDialog(frame, "Failed to add an activity!");
            }
        });

        addButton.setFont(new Font(FONT2, Font.BOLD, 24));
        addActivityPanel.add(addButton);

        JButton btnNewButton = new JButton("Back");
        btnNewButton.addActionListener(e -> {
            addActivityPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });
        btnNewButton.setFont(new Font(FONT1, Font.PLAIN, 22));
        btnNewButton.setBounds(12, 13, 97, 30);
        addActivityPanel.add(btnNewButton);

        JComboBox<String> currencyComboBox = new JComboBox<>(currencyArr);
        currencyComboBox.setBounds(260, 283, 70, 22);
        currencyComboBox.setSelectedIndex(0);
        addActivityPanel.add(currencyComboBox);

        currencyIndex = 0;
        currencyComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                currencyIndex = currencyComboBox.getSelectedIndex();
            }
        });

        JComboBox<String> categoryComboBox = new JComboBox<>(categoryArr);
        categoryComboBox.setBounds(300, 340, 200, 25);
        addActivityPanel.add(categoryComboBox);

        categoryIndex = 0;
        categoryComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                categoryIndex = categoryComboBox.getSelectedIndex();
            }
        });
    }

    /**
     * Initialize the view activity panel
     */
    private void initializeViewActivityPanel() {
        viewActivityPanel = new JPanel();
        viewActivityPanel.setLayout(null);
        frame.getContentPane().add(viewActivityPanel);

        JLabel label = new JLabel("View Activity History");
        label.setFont(new Font("STXinwei", Font.BOLD, 30));
        label.setBounds(125, 61, 400, 32);
        viewActivityPanel.add(label);

        JButton backButton = new JButton(BACKTITLE);
        backButton.addActionListener(e -> {
            viewActivityPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });
        backButton.setFont(new Font(FONT2, Font.BOLD, 24));
        backButton.setBounds(200, 500, 200, 49);
        viewActivityPanel.add(backButton);

        JLabel groupFALabel = new JLabel("Group financial activity");
        groupFALabel.setFont(new Font("Lucida Grande", Font.PLAIN, 15));
        groupFALabel.setBounds(71, 105, 200, 32);
        viewActivityPanel.add(groupFALabel);

        JLabel personalFALabel = new JLabel("Personal financial activity");
        personalFALabel.setFont(new Font("Lucida Grande", Font.PLAIN, 15));
        personalFALabel.setBounds(324, 110, 201, 23);
        viewActivityPanel.add(personalFALabel);

        textArea = new JTextArea();
        textArea.setEditable(false);
        JScrollPane scrollableTextArea = new JScrollPane(textArea);
        scrollableTextArea.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        scrollableTextArea.setBounds(64, 147, 230, 288);
        StringBuilder activityHistoryText = new StringBuilder();

        for (FinancialActivity activity : accountBook.getActivity()) {
            activityHistoryText.append(informationTitle[0] + activity.getActivityName() + "\n");
            activityHistoryText.append(informationTitle[1] + activity.getActivityDate() + "\n");
            activityHistoryText.append(informationTitle[2] + categoryArr[activity.getActivityCategoryId()-accountBook.getCategoryIndexDiff()+1] + "\n");
            activityHistoryText.append(informationTitle[3] + activity.getActivityCost() + "\n");
            activityHistoryText.append("\n");
        }
        textArea.setText(activityHistoryText.toString());
        viewActivityPanel.add(scrollableTextArea);

        JTextArea textArea2 = new JTextArea();
        textArea2.setEditable(false);
        JScrollPane scrollableTextArea2 = new JScrollPane(textArea2);
        scrollableTextArea2.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        scrollableTextArea2.setBounds(310, 147, 230, 288);
        StringBuilder personalActivityHistoryText = new StringBuilder();
        for (FinancialActivity activity : accountBook.getActivity()) {
            if(activity.memberInclude(user.getName())) {
                personalActivityHistoryText.append(informationTitle[0] + activity.getActivityName() + "\n");
                personalActivityHistoryText.append(informationTitle[1] + activity.getActivityDate() + "\n");
                personalActivityHistoryText.append(informationTitle[2] + categoryArr[activity.getActivityCategoryId()-accountBook.getCategoryIndexDiff()+1] + "\n");
                personalActivityHistoryText.append(informationTitle[3] + activity.getCostSplitted() + "\n");
                personalActivityHistoryText.append("\n");
            }
        }
        textArea2.setText(personalActivityHistoryText.toString());
        viewActivityPanel.add(scrollableTextArea2);
    }

    /**
     * Initialize the delete activity panel
     */
    private void initializeDeleteActivityPanel() {
        deleteActivityPanel = new JPanel();
        deleteActivityPanel.setLayout(null);
        frame.getContentPane().add(deleteActivityPanel);

        ArrayList<FinancialActivity> activityList = new ArrayList<>();
        activityList.addAll(accountBook.getActivity());
        String[] activityInfo = new String[activityList.size()+1];
        activityInfo[0] = "*";
        for (int i = 1; i < activityInfo.length; ++i) {
            activityInfo[i] = activityList.get(i-1).getActivityName() + " " + activityList.get(i-1).getActivityDate();
        }
        JComboBox<String> activityListComboBox = new JComboBox<>(activityInfo);
        activityListComboBox.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                activityIndex = activityListComboBox.getSelectedIndex();
                StringBuilder activityInfoText = new StringBuilder();
                if (activityIndex==0) {
                    activityDetail.setText(activityInfoText.toString());
                    return;
                }
                activityInfoText.append(informationTitle[0] + activityList.get(activityIndex-1).getActivityName() + "\n");
                activityInfoText.append(informationTitle[1] + activityList.get(activityIndex-1).getActivityDate() + "\n");
                activityInfoText.append(informationTitle[2] + categoryArr[activityList.get(activityIndex-1).getActivityCategoryId()-accountBook.getCategoryIndexDiff()+1] + "\n");
                activityInfoText.append(informationTitle[3] + activityList.get(activityIndex-1).getActivityCost() + "\n");
                activityInfoText.append("\n");
                activityDetail.setText(activityInfoText.toString());
            }
        });

        JButton button = new JButton(BACKTITLE);
        button.addActionListener(e -> {
            deleteActivityPanel.setVisible(false);
            activityControlPanel.setVisible(true);
        });

        JButton deleteButton = new JButton("Delete");
        deleteButton.addActionListener(e -> {
            if (activityIndex == 0)
                JOptionPane.showMessageDialog(frame, "Please choose an activity!");
            if (accountBook.deleteActivity(activityIndex-1)) {
                JOptionPane.showMessageDialog(frame, "Successfully delete an activity!");
                initializeViewActivityPanel();
                activityListComboBox.removeItemAt(activityIndex);
                deleteActivityPanel.revalidate();
            } else {
                JOptionPane.showMessageDialog(frame, "Failed to delete an activity!");
            }
        });

        JLabel deleteLlabel = new JLabel("Delete Activity");
        deleteLlabel.setHorizontalAlignment(SwingConstants.CENTER);
        deleteLlabel.setFont(new Font(FONT3, Font.BOLD, 30));
        deleteLlabel.setBounds(0, 61, 594, 32);
        deleteActivityPanel.add(deleteLlabel);

        button.setFont(new Font(FONT2, Font.BOLD, 24));
        button.setBounds(200, 500, 200, 49);
        deleteActivityPanel.add(button);

        activityListComboBox.setBounds(44, 189, 322, 30);
        deleteActivityPanel.add(activityListComboBox);

        deleteButton.setFont(new Font(FONT2, Font.BOLD, 24));
        deleteButton.setBounds(394, 177, 156, 49);
        deleteActivityPanel.add(deleteButton);

        activityDetail = new JTextArea();
        activityDetail.setEditable(false);
        activityDetail.setBounds(70, 252, 452, 210);
        deleteActivityPanel.add(activityDetail);
    }

}