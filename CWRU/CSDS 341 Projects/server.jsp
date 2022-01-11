<%@page language="java" import="java.sql.*,java.util.*,java.util.Random,javax.servlet.jsp.*"%>

<%
	Driver DriverRecordset1 = (Driver) Class.forName("org.postgresql.Driver").newInstance();
	Properties props = new Properties();
	props.setProperty("user", "postgres");
	props.setProperty("password", "123456");
	String url = "jdbc:postgresql://localhost/EECS341_project";
	Connection Conn = DriverManager.getConnection(url, props);
	Statement st = Conn.createStatement();
	String  query="select * from Snacks";
	int coloums = 9;
	String isavailable = request.getParameter("isavailable");
	String s_name = request.getParameter("s_name");
	String maxprice = request.getParameter("maxprice");
	String minprice = request.getParameter("minprice");
	
	String nutritionbyname = request.getParameter("nutritionbyname");
	String calories = request.getParameter("calories");
	String sugars = request.getParameter("sugars");
	String allergy_warns = request.getParameter("allergy_warns");
	String caffeine = request.getParameter("caffeine");
	
	String score = request.getParameter("score");
	String snackReviewSName = request.getParameter("snackReviewSName");
	String insertSnackReviewSname = request.getParameter("insertSnackReviewSname");
	String insertSnackReviewScore = request.getParameter("insertSnackReviewScore");
	String insertSnackReviewComments = request.getParameter("insertSnackReviewComments");
	String dateRefill = request.getParameter("dateRefill");
		
	String quantRefil = request.getParameter("quantRefil");
	String comName = request.getParameter("comName");
	String vscore = request.getParameter("vscore");
	String vscore_above = request.getParameter("vscore_above");
	String vReviewsName = request.getParameter("vReviewsName");
		
	String insertvReviewvid = request.getParameter("insertvReviewvid"); 
	String insertvReviewScore = request.getParameter("insertvReviewScore");
	String insertvReviewComments = request.getParameter("insertvReviewComments");
	String building_name = request.getParameter("building_name");
	String region_on_campus = request.getParameter("region_on_campus");
	String vidbybuildingname = request.getParameter("vidbybuildingname");
		
	String isavailablev = request.getParameter("isavailablev");
	String vbys = request.getParameter("vbys");
	
	if (isavailable!=null){
		coloums=9;
		if (isavailable.equals("available")) 
			isavailable="true";
		else 
			isavailable="false";
		query=("select * from Snacks where isavailable='"+isavailable+"'");}
	else if (s_name!=null){
		coloums=9;
		query=("select * from Snacks where s_name='"+s_name+"'");}
	else if (maxprice!=null){
		coloums=2;
		query=("( select s_name, price from Snacks )except( select s_name, price from Snacks where price >= '"+maxprice+"' )");}
	else if (minprice!=null){
		coloums=2;
		query=("select s_name, price from Snacks where not exists (select s_name, price from Snacks where price <= '"+minprice+"')");}
	
	else if (nutritionbyname!=null){
		coloums=6;
		query=("select Snacks.s_name, Snacks.price, Nutrition.calories, Nutrition.allergy_warns, Nutrition.sugars, Nutrition.caffeine from Snacks, Nutrition where Nutrition.s_id=Snacks.s_id and Snacks.s_name = '"+nutritionbyname+"'");}
	else if (calories!=null){
		coloums=3;
		query=("select Snacks.s_name, Snacks.price, Nutrition.calories from Snacks, Nutrition where Nutrition.s_id=Snacks.s_id and Nutrition.calories < '"+calories+"'");}
	else if (allergy_warns!=null){
		coloums=3;
		query=("select Snacks.s_name, Snacks.price, Nutrition.allergy_warns from Snacks, Nutrition where Nutrition.s_id=Snacks.s_id and Nutrition.allergy_warns = '"+allergy_warns+"'");}
	else if (sugars!=null){
		coloums=3;
		query=("select Snacks.s_name, Snacks.price, Nutrition.sugars from Snacks, Nutrition where Nutrition.s_id=Snacks.s_id and Nutrition.sugars < '"+sugars+"'");}
	else if (caffeine!=null){
		coloums=3;
		query=("select Snacks.s_name, Snacks.price, Nutrition.caffeine from Snacks, Nutrition where Nutrition.s_id=Snacks.s_id and Nutrition.caffeine = '"+caffeine+"'");}
	
	else if (score!=null){
		coloums=3;
		query=("select Snack_Review.s_id, Snacks.s_name, Snack_Review.viewer_comments  from Snack_Review, Snacks where Snack_Review.score  = '"+score+"' and Snacks.s_id=Snack_Review.s_id");}	
	else if (snackReviewSName!=null){
		coloums=3;
		query=("select Snacks.s_name, Snack_Review.score, Snack_Review.viewer_comments  from Snack_Review, Snacks where Snacks.s_name = '"+snackReviewSName+"' and Snacks.s_id=Snack_Review.s_id");}
	else if (insertSnackReviewSname!=null){
		coloums=0;
		int r = st.executeUpdate("INSERT INTO Snack_Review ( s_id, score,viewer_comments) SELECT  s_id ,"+insertSnackReviewScore+", '"+insertSnackReviewComments+"' FROM Snacks	WHERE s_name ='"+insertSnackReviewSname+"'");
		out.println("Comments is successfully inserted!");}

	//find the snack name on refill date(enter a date on YYYY-MM-DD)
	else if (dateRefill!=null){
		coloums=2;
		query=("select Snacks.s_name, Refills.date_refill  from  Refills, Snacks where Refills.s_id = Snacks.s_id and Refills.date_refill ='"+dateRefill+"'");}	//find the refill quantity of snack(enter a name)
	else if (quantRefil!=null){
		coloums=2;
		query=("select  Snacks.s_name, Refills.quantity_refill  from  Refills, Snacks  where Refills.s_id = Snacks.s_id and Snacks.s_name ='"+quantRefil+"'");}	//find the company name that refilled the snack (enter a name)
	else if (comName!=null){
		coloums=2;
		query=("select Snacks.s_name, Staff.company_name  from  Staff, Snacks, Refills  where Snacks.s_id = Refills.s_id and Refills.SSN = Staff.SSN and Snacks.s_name = '"+comName+"'");}
	
	else if (isavailablev!=null){
		coloums=8;
		if (isavailablev.equals("available")) 
			isavailablev="true";
		else 
			isavailablev="false";
		query=("select * from Vending_Machine where not exists (select * from Vending_Machine where isavailable<>'"+isavailablev+"')");}
	else if (vbys!=null){
		coloums=17;
		query=("select * from Snacks, Vending_Machine where Snacks.v_id = Vending_Machine.v_id AND Snacks.s_name = '"+vbys+"'");}
	
	else if (building_name!=null){
		coloums=5;
		query=("select * from Location_on_Campus where building_name = '"+building_name+"'");}
	else if (region_on_campus!=null){
		coloums=5;
		query=("(select * from Location_on_Campus) except (select * from Location_on_Campus where region_on_campus <> '"+region_on_campus+"')");}
	else if (vidbybuildingname!=null){
		coloums=2;
		query=("select v_id, Location_on_Campus.building_name from Location_on_Campus, Vending_Machine where Location_on_Campus.building_name = Vending_Machine.building_name AND Location_on_Campus.building_name = '"+vidbybuildingname+"'");}
		
	//search a score
	else if (vscore!=null){
		coloums=2;
		query=("select Vending_Review.v_id, Vending_Review.viewer_comments  from Vending_Review where Vending_Review.score  = '"+vscore+"'");}
	else if (vscore_above!=null){
		coloums=2;
		query=("select vr1.v_id, vr1.viewer_comments from Vending_Review as vr1 where vr1.score  >= '"+vscore_above+"' AND NOT EXISTS (select * from Vending_Review as vr2 where vr2.score  < '"+vscore_above+"' AND vr1.v_id=vr2.v_id)");}
	//	find vending machine score that has a snack name
	else if (vReviewsName!=null){
		coloums=2;
		query=("select Vending_Review.score, Vending_Review.viewer_comments  from Vending_Review where Vending_Review.v_id = '"+vReviewsName+"'");}
	else if (insertvReviewvid!=null){
		coloums=0;
		int r = st.executeUpdate("insert into Vending_Review (v_id,score,viewer_comments) Values ("+insertvReviewvid+","+insertvReviewScore+",'"+insertvReviewComments+"')");
		out.println("Your comments is successfully inserted!");}
	
	ResultSet rs = st.executeQuery(query);
	
%>



<table border = "1">
	<%
		if (!rs.next())
			out.println("Please change the input!");
		else{
	        out.write("<table border='1'>");  
	        out.write("<tr>");  
	        for(int i=1;i<=coloums;i++){  
	            ResultSetMetaData rsmd=rs.getMetaData();  
	            out.write("<th>"+rsmd.getColumnName(i)+"</th>");  
	        }  
	        out.write("</tr>");
			do{
	%>
	<tr>
	<%
			if (coloums!=0){
				int i = 1;
				do{
					%>
					<td><%=rs.getString(i)%></td>
					<%
			    	i++;
				} while (i<=coloums);
			}
	%>
	</tr>
	<%
			} while (rs.next());
		}
	%>
</table>

<%
	rs.close();
	Conn.close();
%>
