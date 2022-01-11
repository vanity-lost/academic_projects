package src;

public class SchemaFields {
	public static final String USERNAME = "username";
	public static final String PASSWORD = "password";
	public static final String CODE = "code";
	public static final String PHONE = "phone";
	public static final String EMAIL = "email";
	public static final String NICKNAME = "nickname";
	public static final String UUID = "id";

	public static final String NAME = "name";
	public static final String BOOK_ID = "bookId";
	public static final String MEMBERS = "members";
	public static final String ENTRY_ID = "entryId";

	public static final String AMOUNT = "amount";
	public static final String DESCRIPTION = "description";
	public static final String DATE = "date";
	public static final String CATEGORY = "category";
	public static final String CATEGORYID = "categoryId";
	public static final String AUTHOR = "author";
	public static final String PARTICIPANTS = "participants";
	public static final String ACCT_BOOK_ID = "accountingBookId";

	public static final String ACCT_BOOK = "accountingBook";

	// REST API headers and schema
	public static final String AUTHOR_HEADER = "Authorization";
	public static final String AUTH_GROUP = "auth";
	public static final String LOGIN_API = "auth";
	public static final String REG_API = "register";
	public static final String RESET_API = "reset";
	public static final String SESSION_API = "me";
	
	public static final String BOOK_HEADER = "book";
	public static final String CREATE_BOOK_API = "create";
	public static final String DEL_BOOK_API = "delete";
	public static final String GET_BOOK_API = "list";
	public static final String MEMBER_API = "member";
	
	private static final String ENTRY_PATH = "entry";
	public static final String ADD_ENT_API = ENTRY_PATH + "/add";
	public static final String DEL_ENT_API = ENTRY_PATH + "/delete";
	public static final String GET_ENT_API = ENTRY_PATH + "/list";
	
	private static final String CATEGORY_PATH = "category";
	public static final String ADD_CAT_API = CATEGORY_PATH + "/add";
	public static final String GET_CAT_API = CATEGORY_PATH + "/list";
}
