import psycopg2
import psqlConfig as config

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        This section establishes a connection to the database with our username and password credentials
        '''

        self.film_list = []

        try:
            establish_connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()

        self.connection = establish_connection




    def getFilmsByTitle(self, title):
        '''
        Returns a list of all of the film titles that include the keywords in the search query

        PARAMETERS:
            Keyword (string)

        RETURNS:
            List of films related to keyword
        '''
        try:
            cursor = self.connection.cursor()
            # The 'UPPER()' functions ensure that it matches titles IGNORING CASING (upper/lowercase) of user's search entry
            query = "SELECT * FROM MoviesOnStreamingPlatforms WHERE REPLACE(UPPER(title), ' ', '') LIKE REPLACE(UPPER(%s), ' ', '')"
            # The '%%' parts ensure that the SQL query script is read as %title%, so that it looks for entries
            # where title is present in ANY part of the title column
            query_details = '%%' + title + '%%'
            cursor.execute(query, (query_details,))

            film_results = cursor.fetchall()
            
            for film in film_results:
                self.film_list.append(film)

            return self.film_list
        except Exception as e:
            print("An error occurred when executing the query: ", e)
            return None

        
    def filterYear(self, film_list, year):
        new_list = []
        
        # If the year filter has been filled out by the user, apply it
        if year != '' and year != ' ':
            for film in film_list:
                if film[1] == int(year):
                    new_list.append(film)
            return new_list
        else:
            return film_list
        
        
    def filterAge(self, film_list, age):
        new_list = []
        
        # If the age filter has been specified by the user, apply it
        if age != "None":
            for film in film_list:
                if film[2] == str(age):
                    new_list.append(film)
            return new_list
        else:
            return film_list
        
    def filterStreamingPlatform(self, film_list, streaming_platform):
        # Finally, if the streaming platform has been specified by the user, apply it, or fill the third layer normally if not
        new_list = []
        
        if streaming_platform != "None":
            if str(streaming_platform) == "netflix":
                for film in film_list:
                    if film[4] == True:
                        new_list.append(film)
                return new_list
            elif str(streaming_platform) == "hulu":
                for film in film_list:
                    if film[5] == True:
                        new_list.append(film)
                return new_list
            elif str(streaming_platform) == "prime-video":
                for film in film_list:
                    if film[6] == True:
                        new_list.append(film)
                return new_list
            elif str(streaming_platform) == "disney-plus":
                for film in film_list:
                    if film[7] == True:
                        new_list.append(film)
                return new_list
        else:
            return film_list
                

if __name__ == '__main__':
    # your code to test your function implementations goes here.
    test = DataSource()

    results = test.getFilmsByTitle('The')

    '''
    results = test.getFilmsByYear('2009')
    results = test.getFilmsOnPrimeVideo('1')
    '''
    results_list = []

    if results is not None:
        # results_list = test.getFilmsByAge('all') [TEST PASSED]
        # results_list = test.getFilmsByYear(2009) [TEST PASSED]
        # results_list = test.getFilmsOnNetflix() [TEST PASSED]
        # results_list = test.getFilmsOnHulu() [TEST PASSED]
        # results_list = test.getFilmsOnPrimeVideo() [TEST PASSED]
        results_list = test.getFilmsOnDisneyPlus()

        for film in results_list:
            film.printFilm()


    '''

    if results is not None:
        print("Query results: ")
        for item in results:
            results_list.append(Film(item))

            display_string = str(item)
            # Because there are some titles with characters not available in ASCII, I encode the string into the
            # UTF-8 codec for more character options
            display_string = display_string.encode('utf-8')
            print(display_string)
    '''
    # Disconnect from database
    test.connection.close()

