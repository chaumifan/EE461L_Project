<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="com.google.appengine.api.users.User" %>
<%@ page import="com.google.appengine.api.users.UserService" %>
<%@ page import="com.google.appengine.api.users.UserServiceFactory" %>
<%@ page import="com.google.appengine.api.datastore.DatastoreServiceFactory" %>
<%@ page import="com.google.appengine.api.datastore.DatastoreService" %>
<%@ page import="com.google.appengine.api.datastore.Query" %>
<%@ page import="com.google.appengine.api.datastore.Entity" %>
<%@ page import="com.google.appengine.api.datastore.FetchOptions" %>
<%@ page import="com.google.appengine.api.datastore.Key" %>
<%@ page import="com.google.appengine.api.datastore.KeyFactory" %>
<%@ page import="com.google.appengine.api.datastore.Query.Filter" %>
<%@ page import="com.google.appengine.api.datastore.Query.FilterOperator" %>
<%@ page import="com.google.appengine.api.datastore.Query.FilterPredicate" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

<html>
  <head>
  	<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
  	<title> Pocket Recipes </title>
    <link rel="shortcut icon" href="static/favicon.ico">
     <!--  Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <link rel=stylesheet type=text/css href="static/css/style.css">
    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script>
      $(document).ready(function(){
        var header = $('#header-img');
        var backgrounds = new Array(
          'static/background3.jpg',
          'static/background2.jpg',
          'static/background.jpg'
        );
        var current = 0;
        function nextBackground() {
            current++;
            current = current % backgrounds.length;
            header.css('background', 'linear-gradient(rgba(19,23,18,0.2),rgba(19,23,18,1)), url(' + backgrounds[current] + ')');
            header.css('background-repeat', 'no-repeat');
            header.css('background-size', '100%');
        }
        setInterval(nextBackground, 3000);
      });
    </script> 
  </head>
  <body>
  <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand">Pocket Recipes</a>
        </div>
        <ul class="nav navbar-nav">
          <li class="active"><a href="#">Browse Recipes</a></li>
          <li><a href="#">Upload Creation</a></li>
        </ul>
        <%
	    UserService userService = UserServiceFactory.getUserService();	
	    User user = userService.getCurrentUser();
	    if (user != null) {
	      pageContext.setAttribute("user", user);
	%>  <ul class="nav navbar-nav navbar-right">
		  <li><a><span class="glyphicon glyphicon-user"></span> Hello, ${fn:escapeXml(user.nickname)}! </a></li>
		  <li><a href="<%= userService.createLogoutURL(request.getRequestURI()) %>"><span class="glyphicon glyphicon-log-out"></span> Log Out</a></li>
		</ul>
	<%
	    } else {
	%>
	    <ul class="nav navbar-nav navbar-right">
	   	  <li><a><span class="glyphicon glyphicon-user"></span> Welcome, guest! </a></li>
	      <li><a href="<%= userService.createLoginURL(request.getRequestURI()) %>"><span class="glyphicon glyphicon-log-in"></span> Log In</a></li>
	    </ul>
	<%
	    }
	%>
      </div>
    </nav>
    <div id=body>
      <div id="header-img" class="jumbotron">
        <div id="title">
          <img id="icon" src="static/icon_burned.png" alt="Card image cap"/>
          <h1> Pocket Recipes </h1>
        </div>
      </div>
      <!-- end header section -->

      <div id="about" class="jumbotron">
        <p>Find recipes that are right for your fridge</p>
      </div>
      <!-- end about section -->

      <div id="grid" class="container">
        <!-- create div to display include ingredients -->
        <div class="row">
          <div class="col-sm-4">
            <!-- search row -->
            <div class="panel panel-success">
              <div class="panel-heading">Specify ingredients you want included in your queries: </div>
              <div class="panel-body">
                <div class=search>
                  <form class="form-inline active-green-4" action ="/add_servlet" method="post">
                    <i class="fa fa-search" aria-hidden="true"></i>
                    <input type="text" class="form-control" placeholder="Include Ingredients" 
                    	id="ingred" name="ingred" style="width: 90%">
                  </form>
                </div>
                <br>
                <!-- dummy ingredient list -->
                <div class="container ingred-list include">
                  <ul class="list-group">
                  	<%
                  	String[] arr = (String[]) request.getAttribute("ingred_list");
                  	if (arr != null) {
                  	  for (int i = 0; i < arr.length; i++) {
                  	  %>
	                    <li class="list-group-item">HELLO
	                      <span class="remove">
	                        <span class="btn btn-sm btn-default" onclick="">
	                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
	                        </span>
	                      </span>
	                    </li>
	                  <%}
	                }%>
                  </ul>
                </div>
              </div>
            </div>
            <!-- end of first panel -->
            <br>
            <!-- create div to display exclude ingredients -->
            <div class="panel panel-danger">
              <div class="panel-heading">Specify ingredients you want excluded in your queries: </div>
              <div class="panel-body">
                <div class=search>
                  <form class="form-inline active-red-4">
                    <i class="fa fa-search" aria-hidden="true"></i>
                    <input type="text" class="form-control" placeholder="Exclude Ingredients" style="width: 90%">
                  </form>
                </div>
                <br>
                <!-- dummy ingredient list -->
                 <div class="container ingred-list exclude">
                  <ul class="list-group">
                    <li class="list-group-item">Cras justo odio
                      <span class="remove">
                        <span class="btn btn-sm btn-default" onclick="">
                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </span>
                      </span>
                    </li>
                    <li class="list-group-item">Dapibus ac facilisis in
                      <span class="remove">
                        <span class="btn btn-sm btn-default" onclick="">
                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </span>
                      </span>
                    </li>
                    <li class="list-group-item">Morbi leo risus
                      <span class="remove">
                        <span class="btn btn-sm btn-default" onclick="">
                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </span>
                      </span>
                    </li>
                    <li class="list-group-item">Porta ac consectetur ac
                      <span class="remove">
                        <span class="btn btn-sm btn-default" onclick="">
                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </span>
                      </span>
                    </li>
                    <li class="list-group-item">Vestibulum at eros
                      <span class="remove">
                        <span class="btn btn-sm btn-default" onclick="">
                          <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </span>
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <!-- end of second panel -->
          </div>

          <div class="col-sm-4">
            <!-- start of recipe panels -->
            <div class="panel panel-info recipes">
              <!-- dummy individual panels -->
              <div class="panel-heading">Card Title</div>
              <img class="panel-img-top" src="https://i.imgur.com/0K4qGqY.jpg" alt="Card image cap">
              <div class="panel-body">
                <h2 class="panel-title">
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star"></span>
                  <span class="fa fa-star"></span>
                </h2>
                <p class="panel-text">Description of recipe, etc.etc.etc...</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
            </div>

            <div class="panel panel-info recipes">
              <!-- dummy individual panels -->
              <div class="panel-heading">Card Title</div>
              <img class="panel-img-top" src="https://i.imgur.com/0K4qGqY.jpg" alt="Card image cap">
              <div class="panel-body">
                <h2 class="panel-title">
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star"></span>
                  <span class="fa fa-star"></span>
                </h2>
                <p class="panel-text">Description of recipe, etc.etc.etc...</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
              <!-- end of dummy data -->
            </div>

          </div>

          <div class="col-sm-4">
            <!-- start of recipe panels -->
            <div class="panel panel-info recipes">
              <!-- dummy individual panels -->
              <div class="panel-heading">Card Title</div>
              <img class="panel-img-top" src="https://i.imgur.com/0K4qGqY.jpg" alt="Card image cap">
              <div class="panel-body">
                <h2 class="panel-title">
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star"></span>
                  <span class="fa fa-star"></span>
                </h2>
                <p class="panel-text">Description of recipe, etc.etc.etc...</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
            </div>

            <div class="panel panel-info recipes">
              <!-- dummy individual panels -->
              <div class="panel-heading">Card Title</div>
              <img class="panel-img-top" src="https://i.imgur.com/0K4qGqY.jpg" alt="Card image cap">
              <div class="panel-body">
                <h2 class="panel-title">
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star checked"></span>
                  <span class="fa fa-star"></span>
                  <span class="fa fa-star"></span>
                </h2>
                <p class="panel-text">Description of recipe, etc.etc.etc...</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
              <!-- end of dummy data -->
            </div>
            
          </div>

        </div>
        <!-- end of row -->
      </div>
      <!-- end of grid -->
    </div>

    <footer class="navbar-default">
      <div class="footer">
        <div class="row">
          <h3><i class="fa fa-facebook"></i>  <i class="fa fa-twitter"></i> <i class="fa fa-envelope"></i> </h3>
          <p>PocketRecipes&#169;</p>
        </div>
      </div>
    </footer>
  </body>
</html>