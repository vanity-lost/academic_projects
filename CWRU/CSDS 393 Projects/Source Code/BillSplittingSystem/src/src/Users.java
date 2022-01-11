package src;

import static java.lang.Math.toIntExact;

import java.io.IOException;
import java.util.*;
import java.util.logging.Logger;
import org.apache.commons.lang3.tuple.Pair;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import io.restassured.response.Response;

/**
 * @author Randolph, Yonghao
 */
@SuppressWarnings("unchecked")
public class Users {
	private static final Logger LOGGER = Logger.getGlobal();

	private static List<Book> books;
	private static String session_id = "";

	private String username;

	public Users() {

	}

	public static String getSession() {
		return session_id;
	}

	public String getName() { return username; }

	/**
	 * @
	 * This method instantiates a user session, invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 * 
	 * @param userInfo The parameters of the user from login.
	 */
	boolean instantiateUser(Map<String, String> userInfo) {
		LOGGER.info("instantiating user session...");
		username = userInfo.get(SchemaFields.USERNAME);
		return postCall(userInfo, RestUtils.formSemiPath(SchemaFields.AUTH_GROUP, SchemaFields.LOGIN_API));
	}

	/**
	 * This method is only invoked from constructor when a new user is created from registration. 
	 * This establishes a current session for the user and passes through database.
	 * 
	 * @param userInfo Values from the registration step
	 */
	boolean createAccount(Map<String, String> userInfo) {
		LOGGER.info("creating account...");
		return postCall(userInfo, RestUtils.formSemiPath(SchemaFields.AUTH_GROUP, SchemaFields.REG_API));
	}

	/**
	 * @
	 * This method instantiates a user session, invoked from frontend and must invoke backend paths for data pass through.
	 * It will call userdbInterface to send dataInfo and check whether is succeeded.
	 *
	 * @param resetInfo The parameters of the user from reset password.
	 */
	boolean resetPassword(Map<String, String> resetInfo) {
		LOGGER.info("resetting account...");
		return postCall(resetInfo, RestUtils.formSemiPath(SchemaFields.AUTH_GROUP, SchemaFields.RESET_API));
	}

	/**
	 * @
	 * This method instantiates a user session, invoked from frontend and must invoke backend paths for data pass through.
	 * It will pass a Map dataInfo and send it through the path to the online databse.
	 *
	 * @param dataInfo The parameters of the user.
	 * @param path The parameters of the path in the database.
	 */
	private boolean postCall(Map<String, String> dataInfo, String path) {
		// REST API fields
		JSONObject obj = new JSONObject();
		obj.putAll(dataInfo);
		// invoke REST API
		try {
			Response res = RestUtils.postCall(path, obj);
			try {
				session_id = RestUtils.getSession(res);
				LOGGER.info("session id= " + session_id);
			} catch (Exception e) {
				LOGGER.info("session id does not exist given method invoke.");
				session_id = "";
			}
			return true;
		} catch (IOException | ServiceRestException e) {
			LOGGER.info("e= " + e);
			return false;
		}
	}

	boolean createBook(String name) {
		LOGGER.info("create book name=" + name);
		JSONObject obj = new JSONObject();
		obj.put(SchemaFields.NAME, name);
		String path = RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.CREATE_BOOK_API);
		Pair<String, String> header = Pair.of("authorization", getSession());
		LOGGER.info("header=" + header.getKey() + " " + header.getValue());
		try {
			RestUtils.postCall(path, obj, header);
			LOGGER.info("done creating book.");
		} catch (Exception e) {
			LOGGER.info("e= " + e);
			return false;
		}

		// update list of Book
		books = getBooks();
		int book_id = books.get(books.size()-1).getID();

		// create four categories
		for (int i = 1; i < MainPageGUI.categoryArr.length; ++i) {
			LOGGER.info("create categories= " + MainPageGUI.categoryArr[i]);
			Map<String, Object> categoryInfo = new HashMap<>();
			categoryInfo.put(SchemaFields.NAME, MainPageGUI.categoryArr[i]);
			categoryInfo.put(SchemaFields.ACCT_BOOK_ID, book_id);
			addCategory(categoryInfo);
		}
		return true;
	}

	boolean addCategory(Map<String, Object> categoryInfo) {
		Pair<String, String> header = Pair.of("authorization", getSession());
		LOGGER.info("add category...");
		JSONObject obj = new JSONObject();
		obj.putAll(categoryInfo);
		try {
			Response res = RestUtils.postCall(RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.ADD_CAT_API), obj, header);
			LOGGER.info(res.asString());
		} catch (IOException | ServiceRestException e) {
			LOGGER.info("e= " + e);
			return false;
		}
		return true;
	}

	List<Book> getBooks() {
		LOGGER.info("getting all books...");
		String path = RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.GET_BOOK_API);
		Pair<String, String> header = Pair.of("authorization", getSession());
		try {
			Response res = RestUtils.getCall(path, header);
			LOGGER.info("done for rest, parsing books...");
			return books = parseBooks(res.asString());
		} catch (Exception e) {
			LOGGER.info("e= " + e);
		}
		return null;
	}

	boolean deleteBook(int index) {
		int bookId = books.get(index).getID();
		LOGGER.info("deleting book id= " + bookId);
		Pair<String, String> header = Pair.of("authorization", getSession());
		try {
			RestUtils.deleteBook(bookId, header);
			books.remove(index);
			LOGGER.info("deleted book");
			return true;
		} catch (Exception e) {
			LOGGER.info("e= " + e);
			return false;
		}
	}


	/**
	 * @
	 * This method will be invoked in the frontend when getting the data about the book storing in the current account. 
	 * it will parse the JSONObject in the response send by the backend to the list of Book
	 *
	 * @param res The response send by the backend.
	 *
	 */
	private List<Book> parseBooks(String res) {
		List<Book> book_list = new ArrayList<Book>();
		JSONObject book_res = new JSONObject();
		JSONParser parser = new JSONParser();
		try {
			book_res = (JSONObject) parser.parse(res);
		} catch (ParseException e) {
			LOGGER.info("error json2str e=" + e);
		}
		JSONArray books = (JSONArray) book_res.get("data");
		if (books == null) {
			return book_list;
		}
		for (Object temp : books) {
			JSONObject b = (JSONObject) temp;
			int id = toIntExact((long) b.get(SchemaFields.UUID));
			String name = (String) b.get(SchemaFields.NAME);
			List<String> ms = new ArrayList<String>();
			JSONArray members = (JSONArray) b.get(SchemaFields.MEMBERS);
			for (int i = 0; i < members.size(); i++) {
				JSONObject m = (JSONObject) members.get(i);
				ms.add((String) m.get(SchemaFields.USERNAME));
			}
			// get the list of all categories
			JSONObject obj = new JSONObject();
			obj.put(SchemaFields.ACCT_BOOK_ID, id);
			String path = RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.GET_CAT_API);
			Pair<String, String> header = Pair.of("authorization", getSession());
			try {
				Response res2 = RestUtils.postCall(path, obj, header);
				LOGGER.info("done get all categories.");
				Book book = new Book(id, name, ms, getEntries(id), getCategoryIndexDiff(res2.asString()));
				book_list.add(book);
			} catch (Exception e) {
				LOGGER.info("e= " + e);
				e.printStackTrace();
				return null;
			}
		}
		return book_list;
	}

	private int getCategoryIndexDiff(String res) {
		JSONObject category_res = new JSONObject();
		JSONParser parser = new JSONParser();
		try {
			category_res = (JSONObject) parser.parse(res);
		} catch (ParseException e) {
			LOGGER.info("error json2str e=" + e);
		}
		JSONArray categories = (JSONArray) category_res.get("data");
		if (categories == null || categories.size()==0)
			return 0;
		JSONObject b = (JSONObject) categories.get(0);
		return toIntExact((long) b.get(SchemaFields.UUID));
	}


	/**
	 * @
	 * This method will be invoked in the frontend and must invoke backend paths for data pass through.
	 * It will return all the financial activities storing in the current accounting books.
	 *
	 * @param id The id of the current accounting book.
	 *
	 */
	static List<FinancialActivity> getEntries(int id) {
		Map<String, Object> entryInfo = new HashMap<>();
		entryInfo.put(SchemaFields.ACCT_BOOK_ID, id);
		JSONObject obj = new JSONObject();
		obj.putAll(entryInfo);
		String path = RestUtils.formSemiPath(SchemaFields.BOOK_HEADER, SchemaFields.GET_ENT_API);
		Pair<String, String> header = Pair.of("authorization", getSession());
		try {
			Response res = RestUtils.postCall(path, obj, header);
			LOGGER.info("done get all entries.");
			return parseEntry(res.asString());
		} catch (Exception e) {
			LOGGER.info("e= " + e);
			e.printStackTrace();
			return null;
		}
	}

	/**
	 * @
	 * This method will be invoked in the frontend when getting the data about the financial activity storing in the current book. 
	 * it will parse the JSONObject in the response send by the backend to the list of financial activity
	 *
	 * @param res The response send by the backend.
	 *
	 */
	private static List<FinancialActivity> parseEntry(String res) {
		List<FinancialActivity> entry_list = new ArrayList<>();
		JSONObject entry_res = new JSONObject();
		JSONParser parser = new JSONParser();
		try {
			entry_res = (JSONObject) parser.parse(res);
		} catch (ParseException e) {
			LOGGER.info("error json2str e=" + e);
		}
		JSONArray entries = (JSONArray) entry_res.get("data");
		if (entries == null || entries.size() == 0) {
			return entry_list;
		}
		for (Object entry : entries) {
			JSONObject e = (JSONObject) entry;
			int id = Math.toIntExact((Long) e.get(SchemaFields.UUID));
			String name = (String) e.get(SchemaFields.DESCRIPTION);
			Double amount = (Double) e.get(SchemaFields.AMOUNT);
			Long date = (Long) e.get(SchemaFields.DATE);
			// get category
			JSONObject categories = (JSONObject) e.get(SchemaFields.CATEGORY);
			int category = Math.toIntExact((Long) categories.get(SchemaFields.UUID));
			// get author
			JSONObject author_obj = (JSONObject) e.get(SchemaFields.AUTHOR);
			String author = (String) author_obj.get(SchemaFields.USERNAME);
			// get participants
			JSONArray parts = (JSONArray) e.get(SchemaFields.PARTICIPANTS);
			List<String> ps = new ArrayList<String>();
			for (Object p : parts) {
				JSONObject jsb = (JSONObject) p;
				ps.add((String) jsb.get(SchemaFields.USERNAME));
			}
			// get acct book id
			JSONObject acctbookID = (JSONObject) e.get(SchemaFields.ACCT_BOOK);
			int bookId = Math.toIntExact((Long) acctbookID.get(SchemaFields.UUID));
			Map<String, Object> m = new HashMap<>();
			m.put(SchemaFields.ENTRY_ID, id);
			m.put(SchemaFields.AMOUNT, amount);
			m.put(SchemaFields.DESCRIPTION, name);
			m.put(SchemaFields.DATE, date);
			m.put(SchemaFields.CATEGORY, category);
			m.put(SchemaFields.AUTHOR, author);
			m.put(SchemaFields.PARTICIPANTS, ps);
			m.put(SchemaFields.ACCT_BOOK_ID, bookId);
			FinancialActivity fa = new FinancialActivity(m);
			entry_list.add(fa);
		}
		return entry_list;
	}

	Book getBookbyID(int book_id) {
		return books.get(book_id);
	}
}
