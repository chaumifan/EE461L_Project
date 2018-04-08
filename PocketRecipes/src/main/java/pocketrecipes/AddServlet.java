package pocketrecipes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

public class AddServlet extends HttpServlet {
	public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		String[] list = (String[])req.getSession().getAttribute("ingred_list");
		String[] arr;
		String ingred = req.getParameter("ingred");
		if (list == null || list.length <= 0) {
			arr = new String[1];
		} else {
			arr = new String[list.length + 1];
			for (int i = 0; i < list.length; i++) {
				arr[i+1] = list[i];
			}
		}
		arr[0] = ingred;
		req.getSession().setAttribute("ingred_list", arr);
		ServletContext context = req.getServletContext();
		RequestDispatcher rd = context.getRequestDispatcher("/landing.jsp");
		try {
			rd.forward(req, resp);
		} catch (ServletException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
