In designing this project, a lot of technical decisions went into play. The reasoning behind the design of this website, its
pages, and the overall flow will be discussed within this document.

The idea behind this project was to implement a website that would allow students and professionals to interact in a quick and
efficient manner. Students would be able to post symptoms they might have been experiencing and professionals can respond with
quick suggestions of whether or not the student should wait some more, or visit the doctor as soon as possible. This project arose
from my own personal struggles with random symptoms and endless questions to my friends of whether or not my symptoms warranted a
trip to the doctor.

The goal of the design of the website was to make the interaction between students and professionals very easy to understand,
with nothing too complicated to get used to. Therefore, a simple registration and login system was employed, almost equivalent to
the one implemented in Finance. The one difference is that there are two different registrations, one for students and one for
professionals. This is because different information is being collected from each type of user, seeing as in the real world, a
professional would first have to be certified before being able to leave suggestions for potential 'patients'.

Each type of user also has a different set of tabs to come upon once they login. This is because each user type has a different
role to play within the website. Students are mainly posting questions and viewing answers. Therefore, their viewable tabs include
"New Question" where they can post new questions and "Pending" where they can see questions that have not yet been answered. Upon
login, a student will see questions that have already been answered. This was done to make it easy for a student to see if their
question has been answered directly upon login, without the need for going to another page.

A professional's main role is to answer questions. Therefore, upon login, they see all unanswered questions. Each question is a
link which leads to a form where the professional can offer a response. It is to note that the professional cannot see which
student asked any question in order to protect the privacy of the student. The professional can also view questions that they
have previously answered under the "History" page. Because a lot of information was collected during the registration of the
professional, a profile tab allows them to see that information.

A "Feedback" tab is available to both students and professionals to allow either to offer feedback on the website. This is
useful to judge how well the website has been implemented and what can be done otherwise. The last tab each user sees is
"Logout" which allows the user to log out.

This site implements many forms and tables because they allow clarity in the collection and presentation of information. There
are a total of 4 SQL tables used to store the information collected by the forms. These include users, questions, answers, and
feedback. It was necessary to have each of these tables in order to clarify the type of information collected. The users table
stores the registration information, with a boolean field called "professional" determining what type of user has registered.
The foreign key joining the questions and answers table is a field called "question_id" which is the primary key for the
questions table. The questions table also keeps track of whether each question has been answered or not, which is useful for
the purposes of tables displaying answered questions and history for students and professionals respectively. The feedback
table anonymously stores the values of each response to the feedback form.

If this website were to be improved, a feature to update a professional's profile would be added. Also, a feature that sends an
email to the student when a professional responds to their question would also be quite useful.

Overall Flow

When a student registers and posts a question, it appears under their pending tab and on the homepage of any registered
professionals. When a professional chooses to answer that question, it appears under their history and on the homepage of the
student.