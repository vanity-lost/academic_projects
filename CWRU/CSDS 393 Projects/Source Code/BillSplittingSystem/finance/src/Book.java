package src;

import java.io.IOException;
import java.util.*;
import java.util.HashMap;
import java.util.logging.Logger;

import org.apache.commons.lang3.tuple.Pair;
import org.json.simple.JSONObject;

public class Book {
	private static final Logger LOGGER = Logger.getGlobal();

	private int bookId;
	private String name;
	private List<String> memberList = new ArrayList<>();
	private List<FinancialActivity> financialActivityList = new ArrayList<>();
	private int categoryIndexDiff;

	public Book() {

	}
	
	public Book(int bookId, String name, List<String> memberList,
				List<FinancialActivity> financialActivityList, int categoryIndexDiff) {
		this.bookId = bookId;
		this.name = name;
		this.memberList = memberList;
		this.financialActivityList = financialActivityList;
		this.categoryIndexDiff = categoryIndexDiff;
	}

	public int getCategoryIndexDiff() {
		return categoryIndexDiff;
	}

	public String getName() {
		return name;
	}

	public int getID() {
		return bookId;
	}
	
	/**
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 * 
	 * @param username The username of each user
	 */
    @SuppressWarnings("unchecked")
	public boolean addMember(String username) {
    	LOGGER.info("adding member..");
		memberList.add(username);
		Pair<String, String> header = Pair.of("authorization", Users.getSession());
		Map<String, Object> memberInfoMap = new HashMap<>();
		memberInfoMap.put(SchemaFields.BOOK_ID, Integer.toString(bookId));
		memberInfoMap.put(SchemaFields.MEMBERS, memberList);
		JSONObject obj = new JSONObject();
		obj.putAll(memberInfoMap);
		try {
			LOGGER.info(obj.toJSONString());
			RestUtils.postCall(RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.MEMBER_API), obj, header);
			LOGGER.info("done.");
		} catch (Exception e) {
			LOGGER.info("e= " + e);
			memberList.remove(username);
			return false;
		}
		return true;
    }

	public List<String> getMemberList() {
		return memberList;
	}

	/**
	 * @
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 *
	 * @param memberIndex The index of the received member list
	 */
	@SuppressWarnings("unchecked")
	public boolean deleteMember(int memberIndex) {
		LOGGER.info("deleting member..");
		Pair<String, String> header = Pair.of("authorization", Users.getSession());
		Map<String, Object> memberInfoMap = new HashMap<>();
		memberInfoMap.put(SchemaFields.BOOK_ID, Integer.toString(bookId));
		memberInfoMap.put(SchemaFields.MEMBERS, memberList);
		JSONObject obj = new JSONObject();
		obj.putAll(memberInfoMap);
		try {
			RestUtils.postCall(RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.MEMBER_API), obj, header);
			memberList.remove(memberIndex);
			LOGGER.info("done.");
		} catch (Exception e) {
			LOGGER.info("e= " + e);
			return false;
		}
		return true;
	}

	/**
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 *
	 * @param activityInfo The values for financial activity
	 */
	public boolean addActivity(HashMap<String, Object> activityInfo){
		LOGGER.info("adding activity...");
		return getResult(activityInfo, RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.ADD_ENT_API));
	}

	@SuppressWarnings("unchecked")
	private boolean getResult(Map<String, Object> activityInfo, String path) {
		// REST API fields
		Pair<String, String> header = Pair.of("authorization", Users.getSession());
		JSONObject obj = new JSONObject();
		obj.putAll(activityInfo);
		// invoke REST API
		try {
			RestUtils.postCall(path, obj, header);
			financialActivityList = Users.getEntries(getID());
			return true;
		} catch (IOException | ServiceRestException e) {
			LOGGER.info("e= " + e);
			return false;
		}
	}

	/**
	 * This method is call for getting the financial activity and must invoke backend paths for data pass through.
	 *
	 */
	public List<FinancialActivity> getActivity() { return financialActivityList; }

	/**
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 *
	 * @param activityIndex The index of the received member list
	 */
	public boolean deleteActivity(int activityIndex) {
		Pair<String, String> header = Pair.of("authorization", Users.getSession());
		LOGGER.info("deleting activity...");
		try {
			RestUtils.deleteEntry(financialActivityList.get(activityIndex).getEntryId(), header);
			financialActivityList.remove(activityIndex);
			return true;
		} catch (IOException e) {
			LOGGER.info("e= " + e);
			return false;
		}
	}
}
