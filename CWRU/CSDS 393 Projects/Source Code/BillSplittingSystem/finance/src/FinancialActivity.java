package src;

import java.text.DecimalFormat;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.time.format.DateTimeParseException;

public class FinancialActivity {

	private int entryId;
	private double cost;    // amount
	private String name;    // description
	private long date;
	private int categoryId;
	private String author;
	private List<String> participants;
	private int accountingBookId;

	private final DecimalFormat df = new DecimalFormat("########.00");

	public FinancialActivity() {

	}
	
	/**
	 * This method is only invoked from frontend to check the format of the parameter passed through.
	 * 
	 * @param name The username of the user
	 */
	
	public boolean isCorrectFormat(String name, String date, String cost) {
		return nameFormat(name) && dateFormat(date) && costFormat(cost);
	}

	private boolean nameFormat(String name) {
		return !(name == null || name.trim() == null);
	}

	private boolean dateFormat(String date) {
		try {
			LocalDate.parse(date);
		} catch (DateTimeParseException e) {
			return false;
		}
		return true;
	}

	private boolean costFormat(String cost) {
		try {
			Double.parseDouble(cost);
		} catch (NullPointerException | NumberFormatException e) {
			return false;
		}
		return true;
	}

	@SuppressWarnings("unchecked")
	public FinancialActivity(Map<String, Object> entryInfo) {
		entryId = (int) entryInfo.get(SchemaFields.ENTRY_ID);
		cost = (double) entryInfo.get(SchemaFields.AMOUNT);
		name = (String) entryInfo.get(SchemaFields.DESCRIPTION);
		date = (long) entryInfo.get(SchemaFields.DATE);
		categoryId = (int) entryInfo.get(SchemaFields.CATEGORY);
		author = (String) entryInfo.get(SchemaFields.AUTHOR);
		participants = (List<String>) entryInfo.get(SchemaFields.PARTICIPANTS);
		setAccountingBookId((int) entryInfo.get(SchemaFields.ACCT_BOOK_ID));
	}

	public String getActivityName() {
		return name;
	}

	public String getActivityDate() {
		return LocalDate.ofEpochDay(date).toString();
	}

	public double getActivityCost() {
		return Double.parseDouble(df.format(cost));
	}

	public int getActivityCategoryId() {
		return categoryId;
	}

	public int getEntryId() {
		return entryId;
	}
	
	/**
	 * This method is only invoked from frontend to get the cost splitting.
	 * it will return the string of the costsplitted
	 * 
	 */
	public String getCostSplitted() {
		return df.format(cost / (participants.size()+1));
	}
	
	/**
	 * This method is only invoked from frontend to check whether the memberList includes the username passed in.
	 * 
	 * @param userName The username going to check
	 */
	public boolean memberInclude(String userName) {
		return author.equals(userName) || participants.contains(userName);
	}

	public int getAccountingBookId() {
		return accountingBookId;
	}

	public void setAccountingBookId(int accountingBookId) {
		this.accountingBookId = accountingBookId;
	}
}