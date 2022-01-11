<html>
	<head><title>EECS341_Project</title></head>
	<body>
		<h1>Snack Tracker</h1>
		
		<h2>Snacks</h2>		
			<form action="server.jsp" method="get">
				Check all snacks: <input type="submit" value="Select"/>
			</form>
			<form action="server.jsp" method="get"> list out <select name="isavailable">
					<option>available</option>
					<option>unavailable</option>
				</select> snacks
				<input type="submit" value="select"/>
			</form>
			<form action="server.jsp" method="get">
				check snacks by name (type name): <input type = "text" name = "s_name">
			</form>
			<form action="server.jsp" method="get">
				find snacks by price (type max price): <input type = "text" name = "maxprice">
			</form>
			
			<form action="server.jsp" method="get">
				find snacks by price (type min price): <input type = "text" name = "minprice">
			</form>
			
		<h2>Nutrition</h2>
			<form action="server.jsp" method="get">
				find snacks nutrition by name (type name): <input type = "text" name = "nutritionbyname">
			</form>
			<form action="server.jsp" method="get">
				find snacks which has calories under: <input type = "text" name = "calories">
			</form>
			<form action="server.jsp" method="get"> 
				find snacks which has allergy_warns or not: <select name="allergy_warns">
					<option>true</option>
					<option>false</option>
				</select> 
				<input type="submit" value="select"/>
			</form>
			<form action="server.jsp" method="get">
				find snacks which has sugars under:  <input type = "text" name = "sugars">
			</form>
			<form action="server.jsp" method="get"> 
				find snacks which has caffeine or not: <select name="caffeine">
					<option>True</option>
					<option>False</option>
				</select> 
				<input type="submit" value="select"/>
			</form>
		
		<h2>Snacks Review</h2>
			<form action="server.jsp" method="get">
				find snacks review of star (range of 1-5): <select name="score">
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
					<option>5</option>
				</select> 
				<input type="submit" value="select"/>
			</form>
			<form action="server.jsp" method="get">
				find snacks review of snack name: <input type = "text" name = "snackReviewSName">
			</form>
			Write your comments:
			<form action="server.jsp" method="get">
				Snacks name: <input type = "text" name = "insertSnackReviewSname"><br>
				Your score (1-5): <input type = "text" name = "insertSnackReviewScore"><br>
				Your comments: <input type = "text" name = "insertSnackReviewComments"><br>
				<input type="submit" value="submit"/>
			</form>
			
		<h2>Staff</h2>
			<form action="server.jsp" method="get">
				find snack name on refill date (enter a date on YYYY-MM-DD): <input type = "text" name = "dateRefill">
			</form>
			<form action="server.jsp" method="get">
				find the refill quality of snacks (enter a name): <input type = "text" name = "quantRefil">
			</form>
			<form action="server.jsp" method="get">
				find the company name that refilled the snack (enter a name): <input type = "text" name = "comName">
			</form>
			
		<h2>Vending Machine</h2>
			<form action="server.jsp" method="get"> 
				list out: <select name="isavailablev">
					<option>available</option>
					<option>unavailable</option>
				</select> vending machine
				<input type="submit" value="select"/>
			</form>
			<form action="server.jsp" method="get">
				find where is your favorite snacks:  <input type = "text" name = "vbys">
			</form>
			
		<h2>Location</h2>
			<form action="server.jsp" method="get">
				find details of the building:  <input type = "text" name = "building_name">
			</form>
			<form action="server.jsp" method="get">
				find all building with vending machine in the region:  <input type = "text" name = "region_on_campus">
			</form>
			<form action="server.jsp" method="get">
				find all vending machine id in this building:  <input type = "text" name = "vidbybuildingname">
			</form>
			
		<h2>Vending Machine Review</h2>
			<form action="server.jsp" method="get">
				find vending machine review of star (range of 1-5): <select name="vscore">				
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
					<option>5</option>
				</select>
				<input type="submit" value="select"/>
			</form>
			<form action="server.jsp" method="get">
				find vending machine with only review above  <select name="vscore_above">				
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
					<option>5</option> 
				</select> stars
				<input type="submit" value="select"/> 
			</form> 
			<form action="server.jsp" method="get">
				find vending machine review of vending machine id: <input type = "text" name = "vReviewsName">
			</form>
			Write your comments:
			<form action="server.jsp" method="get">
				Vending machine's name: <input type = "text" name = "insertvReviewvid"><br>
				Your score (1-5): <input type = "text" name = "insertvReviewScore"><br>
				Your comments: <input type = "text" name = "insertvReviewComments"><br>
				<input type="submit" value="submit"/>
	</body>
</html>
 
