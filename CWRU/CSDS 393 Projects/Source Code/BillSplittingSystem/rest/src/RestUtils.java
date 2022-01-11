package src;

import static io.restassured.RestAssured.*;
import io.restassured.path.json.JsonPath;

import java.io.IOException;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import org.apache.commons.lang3.tuple.Pair;
import org.json.simple.JSONObject;

import io.restassured.response.Response;

@SuppressWarnings("unchecked")
public class RestUtils {
	private static final Logger LOGGER = Logger.getGlobal();
	private static final String API_URI = "https://api.bill.codetector.org";
	public static final String CONTENT_TYPE = "Content-Type";
	public static final String JSON_HEADER = "application/json";
	public static final int SUCCESS_STATUS = 200;
	
	private static final String TESTCLASS_SUFFIX = "Test";
	
	/*
	 * Utility classes should never be instantiated.
	 */
	private RestUtils() {
		// left blank intentionally to prevent instantiation.
	}
	
	static String getClassname(String classname) {
		return classname.substring(0, classname.length() - TESTCLASS_SUFFIX.length()).toLowerCase();
	}
	
	
	/**
	 * it will concat the input strings to form the full path of API
	 * 
	 * @param paths The multiple string objects
	 */
	static String formFullPath(String... paths) {
		String fullpath = API_URI;
		for (String path : paths) {
			fullpath = fullpath + "/" + path; 
		}
		return fullpath;
	}
	
	/**
	 * it will concat the input strings to form the Semi path of API
	 * 
	 * @param paths The multiple string objects
	 */
	static String formSemiPath(String... subpaths) {
		String subpath = "";
		for (String sp : subpaths) {
			subpath += ("/" + sp);
		}
		return subpath;
	}
	
	static String getSession(Response res) {
		LOGGER.info("getting session token...");
		String session_id = "";
		session_id = JsonPath.with(res.asString()).get("data.token");
		return session_id;
	}
	
	static Map<String, String> getCurrentSessionUser() {
		String s_id = Users.getSession();
		Response res = getCall(RestUtils.formSemiPath(SchemaFields.AUTH_GROUP, SchemaFields.SESSION_API), Pair.of(SchemaFields.AUTHOR_HEADER, s_id));
		Map<String, String> m = new HashMap<String, String>();
		m.put(SchemaFields.USERNAME, JsonPath.with(res.asString()).get("data.account.username"));
		m.put(SchemaFields.NICKNAME, JsonPath.with(res.asString()).get("data.account.nickname"));
		m.put(SchemaFields.EMAIL, JsonPath.with(res.asString()).get("data.account.email"));
		m.put(SchemaFields.PHONE, JsonPath.with(res.asString()).get("data.account.phone"));
		return m;
	}
	
	static Response getCall(String path) {
		Response res = given()
				.when()
				.get(API_URI + path);
		return res;
	}
	
	static Response getCall(String path, Pair<String, String> headers) {
		Response res = given()
				.header(headers.getKey(), headers.getValue())
				.when()
				.get(API_URI + path);
		LOGGER.info("res= " + res.asString());
		return res;
	}
	
	/**
	 * @
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will pass a Map dataInfo and send it through the path to the online databse.
	 *
	 * @param obj The JSONObject data we want to pass.
	 * @param path The parameters of the path in the database.
	 */
	
	static Response postCall(String path, JSONObject obj) throws ServiceRestException, IOException {
		Response res = given()
				.header(CONTENT_TYPE, JSON_HEADER) // ("Content-Type","application/json" )
				.body(jsonToString(obj))
				.when()
				.post(API_URI + path);
		LOGGER.info("res= " + res.asString());
		if (res.getStatusCode() != SUCCESS_STATUS) {
			LOGGER.info("res= " + res.asString());
			throw new ServiceRestException("POST unsuccessful.");
		}
		return res;
	}
	
	/**
	 * @
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will pass a Map dataInfo and send it through the path to the online databse.
	 *
	 * @param obj The JSONObject data we want to pass.
	 * @param path The parameters of the path in the database.
	 * @param header The header information in the form of Pair.
	 */
	
	static Response postCall(String path, JSONObject obj, Pair<String, String> header) throws IOException, ServiceRestException {
		Response res = given()
				.header(CONTENT_TYPE, JSON_HEADER)
				.header(header.getKey(), header.getValue()) //("authorization","47ee53f1-ec42-4d1d-abf5-b689f7e808cf")
				.body(jsonToString(obj))	// ("name":"benbook1")
				.when()
				.post(API_URI + path);
		LOGGER.info("res= " + res.asString());
		if (res.getStatusCode() != SUCCESS_STATUS) {
			LOGGER.info("res= " + res.asString());
			throw new ServiceRestException("POST unsuccessful.");
		}
		return res;
	}
	
	/**
	 * @
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will delete the data about the user in the database
	 *
	 * @param username The username we want to delete in the database.
	 */
	static void deleteCall(String username) throws IOException {
		JSONObject obj = new JSONObject();
		obj.put(SchemaFields.USERNAME, username);
		given()
		.header(CONTENT_TYPE, JSON_HEADER)
		.body(jsonToString(obj))
		.when()
		.delete(API_URI + "/auth/test_delete");
	}
	
	/**
	 * @
	 * This method is invoked from frontend and must invoke backend paths for data pass through.
	 * It will delete the data about the accounting book in the database
	 *
	 * @param entry_id The entryID of the accounting book we want to delete.
	 * @param header The header information in the form of Pair
	 */
	
	static void deleteEntry(int entry_id, Pair<String, String> header) throws IOException {
		JSONObject obj = new JSONObject();
		obj.put(SchemaFields.ENTRY_ID, entry_id);
		given()
		.header(CONTENT_TYPE, JSON_HEADER)
				.header(header.getKey(), header.getValue())
		.body(jsonToString(obj))
		.when()
		.delete(API_URI + "/book/entry/delete");
	}
	
	static Response deleteBook(int book_id, Pair<String, String> header) throws IOException {
		JSONObject obj = new JSONObject();
		obj.put(SchemaFields.BOOK_ID, book_id);
		Response res = given()
		.header(CONTENT_TYPE, JSON_HEADER)
				.header(header.getKey(), header.getValue())
		.body(jsonToString(obj))
		.when()
		.delete(API_URI + "/book/delete");
		return res;
	}

	private static String jsonToString(JSONObject obj) throws IOException {
		StringWriter output = new StringWriter();
		try {
			obj.writeJSONString(output);
			return output.toString();
		} catch (IOException e) {
			// we want to avoid using e.printStackTrace(), instead use LOGGER.info("e= " + e);
			LOGGER.info("e= " + e);
			throw new IOException("error in json to string.");
		}
	}
}
