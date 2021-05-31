import psycopg2
from flask import Flask, render_template, request


app = Flask(__name__)
con = psycopg2.connect(database="Crime", user="postgres", password="root", host="localhost", port="5432")
# con = psycopg2.connect(database="group_12", user="group_12", password="VXpqAAAmP7cip", host="10.17.5.99", port="5432")
cursor = con.cursor()
# import pprint

@app.route("/", methods=['post', 'get'])
@app.route("/home", methods=['post', 'get'])
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/auto_theft", methods=['post', 'get'])
def auto_theft():
    if request.method == 'POST':
        query_temp="SELECT DISTINCT group_name FROM auto_theft"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM auto_theft ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])
        
        if "states" in request.form:
            state = request.form['states']
            # print(state)
            query1 = "SELECT * FROM auto_theft WHERE area_name = '"+state+"' ORDER BY year ASC, group_name ASC"
            cursor.execute(query1)
            result1 = cursor.fetchall()

            # query2 = "SELECT year, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC"
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"') as y "
            query2 += "ORDER BY year ASC"
            cursor.execute(query2)
            result2 = cursor.fetchall()

            query3 = "SELECT group_name, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"' GROUP BY group_name ORDER BY group_name ASC"
            cursor.execute(query3)
            result3 = cursor.fetchall()

            
            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(auto_theft_coordinated_traced,0),COALESCE(auto_theft_recovered,0),COALESCE(auto_theft_stole,0) FROM auto_theft WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    # print(result_temp)
                    if len(result_temp)==0:
                        x_data[i][0].append(0)
                        x_data[i][1].append(0)
                        x_data[i][2].append(0)
                        continue
                    x_data[i][0].append(result_temp[0][0])
                    x_data[i][1].append(result_temp[0][1])
                    x_data[i][2].append(result_temp[0][2])
                    # break
            # print("------------------")
            # print(year_types)
            # print("------------------")
            # print(group_types)
            # print("------------------")
            # print(x_data[0])
            # print("------------------")
            # print(x_data['Goods carrying vehicles (Trucks/Tempo etc)'])
            # print("------------------")
            # x_data_final = []
            # for group in group_types:
            #     temp = {}
            #     temp[label]: 'Cases_Reported'
            return render_template('auto_theft.html', state = state, result1 = result1, result2 = result2, result3 = result3, y_data=year_types, x_data=x_data, group_types=group_types) 

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            # print(compare_area)
            # print(compare_year)
            # print(compare_type)
            query = "SELECT * FROM auto_theft "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(group_Name = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR group_Name = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY year ASC, group_name ASC, area_name ASC"
            # print(query)
            cursor.execute(query)
            result = cursor.fetchall()

            
            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(compare_type):
                    x_data.append([])
                    # print(i,type)
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(auto_theft_stole,0) FROM auto_theft WHERE group_name='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp, result[0][0])
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            print(x_data_all)
            print(len(x_data_all))
            print(compare_type)
            print(compare_year)
            return render_template('auto_theft.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result, types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        return render_template('auto_theft.html')


@app.route("/serious_fraud", methods=['post', 'get'])
def serious_fraud():
    if request.method == 'POST':
        # print("post")
        query_temp="SELECT DISTINCT group_name FROM serious_fraud"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM serious_fraud ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])
        
        if "states" in request.form:
            print("x")
            state = request.form['states']

            query2 = "SELECT DISTINCT group_name FROM serious_fraud"
            cursor.execute(query2)
            result2 = cursor.fetchall()

            result = []

            for r in result2:
                query_temp = "SELECT * FROM serious_fraud WHERE area_name = '"+state+"' AND group_name = '"+r[0]+"' ORDER BY year ASC"
                cursor.execute(query_temp)
                result_temp = cursor.fetchall()
                result.append({'group_name' : r[0], 'result' : result_temp})
            # print(result)
            query1 = "SELECT * FROM serious_fraud WHERE area_name = '"+state+"' ORDER BY year ASC"
            cursor.execute(query1)
            result1 = cursor.fetchall()

            query2 = "SELECT year,a,b,c,d,e,a+b+c+d+e as f FROM (SELECT year, COALESCE(sum(loss_of_Property_1_10_Crores),0) as a, COALESCE(sum(loss_of_Property_10_25_Crores),0) as b, COALESCE(sum(loss_of_Property_25_50_Crores),0) as c, COALESCE(sum(loss_of_Property_50_100_Crores),0) as d, COALESCE(sum(loss_of_Property_Above_100_Crores),0) as e FROM serious_fraud WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC) AS z"
            cursor.execute(query2)
            result2 = cursor.fetchall()

            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[],[],[],[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(loss_of_property_1_10_crores,0)+COALESCE(loss_of_property_10_25_crores,0)+COALESCE(loss_of_property_25_50_crores,0)+COALESCE(loss_of_property_50_100_crores,0)+COALESCE(loss_of_property_above_100_crores,0) FROM serious_fraud WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    print(result_temp)
                    if len(result_temp)==0:
                        x_data[i][0].append(0)
                    else:
                        x_data[i][0].append(result_temp[0][0])

                    query_temp = "SELECT COALESCE(loss_of_property_1_10_crores,0),COALESCE(loss_of_property_10_25_crores,0),COALESCE(loss_of_property_25_50_crores,0),COALESCE(loss_of_property_50_100_crores,0),COALESCE(loss_of_property_above_100_crores,0) FROM serious_fraud WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    # print(result_temp)
                    if len(result_temp)==0:
                        # print(year,result_temp)
                        x_data[i][5].append(0)
                        x_data[i][1].append(0)
                        x_data[i][2].append(0)
                        x_data[i][3].append(0)
                        x_data[i][4].append(0)
                        continue
                    x_data[i][5].append(result_temp[0][4])
                    x_data[i][1].append(result_temp[0][0])
                    x_data[i][2].append(result_temp[0][1])
                    x_data[i][3].append(result_temp[0][2])
                    x_data[i][4].append(result_temp[0][3])

            print("------------------")
            print(x_data)
            print("------------------")
            print(year_types)
            print("------------------")
            print(group_types)
            print("------------------")
            print(year_types)

            return render_template('serious_fraud.html',state = state, result = result, result1 = result1, result2 = result2, y_data=year_types, x_data=x_data, group_types=group_types)

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            query = "SELECT * FROM serious_fraud "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(group_Name = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR group_Name = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY year ASC, group_name ASC, area_name ASC"
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()


            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(group_types):
                    x_data.append([])
                    print(i,"-",t,"-")
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(loss_of_property_1_10_crores,0)+COALESCE(loss_of_property_10_25_crores,0)+COALESCE(loss_of_property_25_50_crores,0)+COALESCE(loss_of_property_50_100_crores,0)+COALESCE(loss_of_property_above_100_crores,0) FROM serious_fraud WHERE group_name='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        # print(query_temp)
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp)
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            print(x_data_all)
            print(len(x_data_all))
            print(compare_type)
            print(compare_year)
            return render_template('serious_fraud.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result, types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        # print("get")
        return render_template('serious_fraud.html')


@app.route("/murder_victim_age_sex", methods=['post', 'get'])
def murder_victim_age_sex():
    if request.method == 'POST':
        query_temp="SELECT DISTINCT group_name FROM murder_victim_age_sex"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM murder_victim_age_sex ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])

        if 'states' in request.form:
            state = request.form['states']

            query1 = "SELECT DISTINCT group_name FROM murder_victim_age_sex"
            cursor.execute(query1)
            result1 = cursor.fetchall()

            result = []

            for r in result1:
                query_temp = "SELECT * FROM murder_victim_age_sex WHERE area_name = '"+state+"' AND group_name = '"+r[0]+"' ORDER BY year ASC"
                cursor.execute(query_temp)
                result_temp = cursor.fetchall()
                result.append({'group_name' : r[0], 'result' : result_temp})

            query2 = "SELECT * FROM murder_victim_age_sex WHERE area_name = '"+state+"' ORDER BY year ASC, Group_name ASC"
            cursor.execute(query2)
            result2 = cursor.fetchall()



            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[],[],[],[],[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(victims_upto_10_yrs,0),COALESCE(victims_upto_10_15_yrs,0),COALESCE(victims_upto_15_18_yrs,0),COALESCE(victims_upto_18_30_yrs,0),COALESCE(victims_upto_30_50_yrs,0),COALESCE(victims_above_50_yrs,0),COALESCE(victims_total,0) FROM murder_victim_age_sex WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    # print(result_temp)
                    if len(result_temp)==0:
                        print(year,result_temp)
                        x_data[i][0].append(0)
                        x_data[i][1].append(0)
                        x_data[i][2].append(0)
                        x_data[i][3].append(0)
                        x_data[i][4].append(0)
                        x_data[i][5].append(0)
                        x_data[i][6].append(0)
                        continue
                    x_data[i][0].append(result_temp[0][0])
                    x_data[i][1].append(result_temp[0][1])
                    x_data[i][2].append(result_temp[0][2])
                    x_data[i][3].append(result_temp[0][3])
                    x_data[i][4].append(result_temp[0][4])
                    x_data[i][5].append(result_temp[0][5])
                    x_data[i][6].append(result_temp[0][6])

            print("------------------")
            print(x_data)
            print("------------------")
            print(year_types)
            print("------------------")
            print(group_types)
            print("------------------")
            return render_template('murder_victim_age_sex.html',state = state, result = result, result1 = result1, result2 = result2, y_data=year_types, x_data=x_data, group_types=group_types)

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            query = "SELECT * FROM murder_victim_age_sex "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(group_Name = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR group_Name = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY year ASC, group_name ASC, area_name ASC"
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(group_types):
                    x_data.append([])
                    print(i,"-",t,"-")
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(victims_total,0) FROM murder_victim_age_sex WHERE group_name='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        # print(query_temp)
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp)
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            print(x_data_all)
            print(len(x_data_all))
            print(compare_type)
            print(compare_year)
            return render_template('murder_victim_age_sex.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result, types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        return render_template('murder_victim_age_sex.html')


@app.route("/all", methods=['post', 'get'])
def all():
    if request.method == 'POST':
        states = request.form.getlist('states')
        query = ""
        for i in range(0,len(states),1):
            # print(states[i])
            query += " select area_name as state, 'Total Automobile Thefts' as crime, (sum(auto_theft_coordinated_traced) + sum(auto_theft_recovered) + sum(auto_theft_stole)) as cases from auto_theft where area_name='"+states[i]+"' group by area_name"
            query += " union all"
            query += " select area_name as state, 'Total Serious Fraud' as crime, (sum(loss_of_property_1_10_crores)+sum(loss_of_property_10_25_crores)+sum(loss_of_property_25_50_crores)+sum(loss_of_property_50_100_crores)+sum(loss_of_property_above_100_crores)) as cases from serious_fraud where area_name='"+states[i]+"' group by area_name"
            query += " union all"
            query += " select area_name as state, 'Total murders' as crime, sum(victims_total) as cases from murder_victim_age_sex where area_name = '"+states[i]+"' and group_name = 'Total Victims' group by area_name"
            query += " union all"
            query += " select area_name as state, 'Total Rapes ' as crime, sum(victims_of_rape_total) as cases from victims_of_rape where area_name = '"+states[i]+"' group by area_name"
            query += " union all"
            query += " select area_name as state, 'Other Crimes Against Women Reported' as crime, sum(cases_Reported) as cases from cases_under_crime_against_women where area_name = '"+states[i]+"' group by area_name"
            query += " union all"
            query += " select area_name as state, 'Other Crimes Against Women In Trial' as crime, sum(cases_Sent_for_Trial) as cases from cases_under_crime_against_women where area_name = '"+states[i]+"' group by area_name"
            if(i+1<len(states)):
                query += " union all"
        # print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        # print(result)
        return render_template('all.html', states = states, result=result)
    else:
        return render_template('all.html')


@app.route("/register", methods=['post', 'get'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(username,password)
        query = "SELECT * FROM users WHERE username='"+username+"'"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result)==0:
            query = "INSERT INTO users (username,password) VALUES ('"+username+"','"+password+"')"
            cursor.execute(query)
            con.commit()
            return render_template('register.html', success="true")
        else:
            return render_template('register.html', already_taken=username)
        
        return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/login", methods=['post', 'get'])
def login():
    if request.method == 'POST':
        print("yy")
        query = "SELECT * FROM users WHERE username='"+request.form.get("username")+"' and password='"+request.form.get("password")+"'"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result)==0:
            print("fail")
            return render_template('login.html', login_fail="true")
        else:
            if 'auto_theft' in request.form:
                query = "INSERT INTO auto_theft (area_name,year,group_name,auto_theft_coordinated_traced,auto_theft_recovered,auto_theft_stole) VALUES ('"+request.form.get("auto_theft")+"','"+request.form.get("year")+"','"+request.form.get("group_name")+"','"+request.form.get("auto_theft_coordinated_traced")+"','"+request.form.get("auto_theft_recovered")+"','"+request.form.get("auto_theft_stole")+"')"                         
                print(query)
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")

            elif 'serious_fraud' in request.form:
                query = "INSERT INTO serious_fraud (area_name,year,group_name,loss_of_property_1_10_crores,loss_of_property_10_25_crores,loss_of_property_25_50_crores,loss_of_property_50_100_crores,loss_of_property_above_100_crores) VALUES ('"+request.form.get("serious_fraud")+"','"+request.form.get("year")+"','"+request.form.get("group_name")+"','"+request.form.get("loss_of_property_1_10_crores")+"','"+request.form.get("loss_of_property_10_25_crores")+"','"+request.form.get("loss_of_property_25_50_crores")+"','"+request.form.get("loss_of_property_50_100_crores")+"','"+request.form.get("loss_of_property_above_100_crores")+"')"                         
                print(query)
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")
            
            elif 'murder_victim_age_sex' in request.form:
                a = request.form.get("murder_victim_age_sex")
                b = request.form.get("year")
                c = request.form.get("group_name")
                d = request.form.get("victims_upto_10_yrs")
                e = request.form.get("victims_upto_10_15_yrs")
                f = request.form.get("victims_upto_15_18_yrs")
                g = request.form.get("victims_upto_18_30_yrs")
                h = request.form.get("victims_above_50_yrs")
                i = int(d)+int(e)+int(f)+int(g)+int(h)
                query = "INSERT INTO murder_victim_age_sex VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"','"+str(i)+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")

            elif 'crime_against_women' in request.form:
                a = request.form.get("crime_against_women")
                b = request.form.get("year")
                c = request.form.get("group_name")
                d = request.form.get("cases_reported")
                e = request.form.get("cases_sent_for_trial")
                query = "INSERT INTO cases_under_crime_against_women (area_name ,year ,group_name ,cases_reported ,cases_sent_for_trial ) VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")

            elif 'arrestsIn_crime_against_women' in request.form:
                a = request.form.get("arrestsIn_crime_against_women")
                b = request.form.get("year")
                c = request.form.get("group_name")
                d = request.form.get("persons_arrested")
                e = request.form.get("persons_convicted")
                query = "INSERT INTO arrests_under_crime_against_women (area_name ,year ,group_name ,persons_arrested ,persons_convicted ) VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")
                
            elif 'rape_cases' in request.form:
                a = request.form.get("rape_cases")
                b = request.form.get("year")
                c = request.form.get("group_name")
                d = request.form.get("victims_upto_10_yr")
                e = request.form.get("victims_between_10_14_yrs")
                f = request.form.get("victims_between_14_18_yrs")
                g = request.form.get("victims_between_18_30_yrs")
                h = request.form.get("victims_between_30_50_yrs")
                i = request.form.get("victims_above_50_yrs")
                j = int(d)+int(e)+int(f)+int(g)+int(h)+int(i)
                query = "INSERT INTO victims_of_rape (area_name ,year ,subgroup ,victims_upto_10_yr ,victims_between_10_14_yrs,victims_between_14_18_yrs,victims_between_18_30_yrs,victims_between_30_50_yrs,victims_above_50_yrs,victims_of_rape_total) VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"','"+str(j)+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")
            
            elif 'trial_of_violent_crimes2' in request.form:
                a = request.form.get("trial_of_violent_crimes2")
                b = request.form.get("year")
                c = request.form.get("group_name")
                d = request.form.get("trial_of_violent_crimes_by_courts_by_confession")
                e = request.form.get("trial_of_violent_crimes_by_courts_by_trial")
                f = int(d)+int(e)
                query = "INSERT INTO trial_of_violent_crimes_by_courts VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+str(f)+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")

            elif 'period_of_trials2' in request.form:
                a = request.form.get("period_of_trials2")
                b = request.form.get("year")
                c = request.form.get("sub_group_name")
                d = request.form.get("pt_1_3_years")
                e = request.form.get("pt_3_5_years")
                f = request.form.get("pt_5_10_years")
                g = request.form.get("pt_6_12_months")
                h = request.form.get("pt_less_than_6_months")
                i = request.form.get("pt_over_10_years")
                j = int(d)+int(e)+int(f)+int(g)+int(h)+int(i)
                query = "INSERT INTO period_of_trials_by_courts VALUES ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"','"+str(j)+"')"                         
                cursor.execute(query)
                con.commit()
                return render_template('login.html', login_success="true")
        return render_template('login.html')
    else:
        return render_template('login.html')


# -----------------------------------------------  UTSAV CODE-------------


@app.route("/crime_against_women", methods=['post', 'get'])
def crime_against_women():

    if request.method == 'POST':
        query_temp="SELECT DISTINCT group_name FROM cases_under_crime_against_women"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM cases_under_crime_against_women ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])
        if "states" in request.form:
            state = request.form['states']
            print(state)
            query1 = "SELECT area_name, year, 	group_Name, cases_Reported, cases_Sent_for_Trial "
            query1 = query1 + "FROM cases_under_crime_against_women WHERE area_name = '"+state+"' ORDER BY year ASC, group_name ASC"
            print(query1)
            cursor.execute(query1)
            result1 = cursor.fetchall()

            # query2 = "SELECT year, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC"
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, sum(cases_Reported), sum(cases_Sent_for_Trial) FROM cases_under_crime_against_women WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(cases_Reported), sum(cases_Sent_for_Trial) FROM cases_under_crime_against_women WHERE area_name = '"+state+"') as y "
            query2 += "ORDER BY year ASC"
            print("query2")
            print(query2)
            cursor.execute(query2)
            result2 = cursor.fetchall()
            year_val = [];
            t2_1 = [];
            t2_2 = [];
            for r in range(len(result2)-1):
                year_val.append(result2[r][0]);
                t2_1.append(result2[r][1]);
                t2_2.append(result2[r][2]);

            query3 = "SELECT group_name, sum(cases_Reported), sum(cases_Sent_for_Trial) FROM cases_under_crime_against_women WHERE area_name = '"+state+"' GROUP BY group_name ORDER BY group_name ASC"
            cursor.execute(query3)
            result3 = cursor.fetchall()

            y_val = [];
            t3_1 = [];
            t3_2 = [];
            for r in result3:
                y_val.append(r[0]);
                t3_1.append(r[1]);
                t3_2.append(r[2]);




                
            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(cases_Reported,0),COALESCE(cases_Sent_for_Trial,0) FROM cases_under_crime_against_women WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    print(result_temp)
                    if len(result_temp)==0:
                        x_data[i][0].append(0)
                        x_data[i][1].append(0)
                        continue
                    x_data[i][0].append(result_temp[0][0])
                    x_data[i][1].append(result_temp[0][1])
            return render_template('crime_against_women.html', state = state, result1 = result1,result2=result2, result3= result3,year_val=year_val,t2_1=t2_1,t2_2=t2_2,y_val=y_val,t3_1=t3_1,t3_2=t3_2,y_data=year_types, x_data=x_data, group_types=group_types)  

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            query = "SELECT area_name, year, group_Name, cases_Reported, cases_Sent_for_Trial "
            query = query + "FROM cases_under_crime_against_women "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(group_Name = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR group_Name = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY area_name ASC, year ASC, group_name ASC"
            print("query= "+ query)
            cursor.execute(query)
            result = cursor.fetchall()


            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(compare_type):
                    x_data.append([])
                    # print(i,type)
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(cases_Sent_for_Trial,0) FROM cases_under_crime_against_women WHERE group_name='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp, result[0][0])
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            print(x_data_all)
            print(len(x_data_all))
            print(compare_type)
            print(compare_year)

            return render_template('crime_against_women.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result, types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        return render_template('crime_against_women.html')


@app.route("/arrestsIn_crime_against_women", methods=['post', 'get'])
def arrestsIn_crime_against_women():
    if request.method == 'POST':
        query_temp="SELECT DISTINCT group_name FROM arrests_under_crime_against_women"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM arrests_under_crime_against_women ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])
        if "states" in request.form:
            state = request.form['states']
            print(state)
            query1 = "SELECT area_name, year, 	group_Name,persons_arrested, persons_convicted "
            query1 = query1 + "FROM arrests_under_crime_against_women WHERE area_name = '"+state+"' ORDER BY year ASC, group_name ASC"
            print(query1)
            cursor.execute(query1)
            result1 = cursor.fetchall()

            # query2 = "SELECT year, sum(Auto_theft_coordinated_traced), sum(Auto_theft_recovered), sum(Auto_theft_stole) FROM auto_theft WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC"
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, sum(persons_arrested), sum(persons_convicted) FROM arrests_under_crime_against_women WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(persons_arrested), sum(persons_convicted) FROM arrests_under_crime_against_women WHERE area_name = '"+state+"') as y "
            query2 += "ORDER BY year ASC"
            print("query2")
            print(query2)
            cursor.execute(query2)
            result2 = cursor.fetchall()
            year_val = [];
            t2_1 = [];
            t2_2 = [];
            for r in range(len(result2)-1):
                year_val.append(result2[r][0]);
                t2_1.append(result2[r][1]);
                t2_2.append(result2[r][2]);

            query3 = "SELECT group_name, sum(persons_arrested), sum(persons_convicted) FROM arrests_under_crime_against_women WHERE area_name = '"+state+"' GROUP BY group_name ORDER BY group_name ASC"
            cursor.execute(query3)
            result3 = cursor.fetchall()

            y_val = [];
            t3_1 = [];
            t3_2 = [];
            for r in result3:
                y_val.append(r[0]);
                t3_1.append(r[1]);
                t3_2.append(r[2]);

            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(persons_arrested,0),COALESCE(persons_convicted,0) FROM arrests_under_crime_against_women WHERE group_name='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    print(result_temp)
                    if len(result_temp)==0:
                        x_data[i][0].append(0)
                        x_data[i][1].append(0)
                        continue
                    x_data[i][0].append(result_temp[0][0])
                    x_data[i][1].append(result_temp[0][1])

            return render_template('arrestsIn_crime_against_women.html', state = state, result1 = result1,result2=result2, result3= result3,year_val=year_val,t2_1=t2_1,t2_2=t2_2,y_val=y_val,t3_1=t3_1,t3_2=t3_2,y_data=year_types, x_data=x_data, group_types=group_types) 

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)    
            query = "SELECT area_name, year, group_Name,persons_arrested, persons_convicted "
            query = query + "FROM arrests_under_crime_against_women "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(group_Name = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR group_Name = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY  year ASC, group_name ASC,area_name ASC"
            print("query= "+ query)
            cursor.execute(query)
            result = cursor.fetchall()

            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(compare_type):
                    x_data.append([])
                    # print(i,type)
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(persons_convicted,0) FROM arrests_under_crime_against_women WHERE group_name='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp, result[0][0])
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            return render_template('arrestsIn_crime_against_women.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result, types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        return render_template('arrestsIn_crime_against_women.html')


@app.route("/rape_cases", methods=['post', 'get'])
def rape_cases():
    if request.method == 'POST':
        query_temp="SELECT DISTINCT subgroup FROM victims_of_rape"
        group_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            group_types.append(r[0])

        query_temp="SELECT DISTINCT year FROM victims_of_rape ORDER BY year"
        year_types=[]
        cursor.execute(query_temp)
        result = cursor.fetchall()
        for r in result:
            year_types.append(r[0])
        if "states" in request.form:
            state = request.form['states']
            print(state)
            query1 = "SELECT year, subgroup,victims_upto_10_yr, victims_between_10_14_yrs, victims_between_14_18_yrs,victims_between_18_30_yrs, victims_between_30_50_yrs, victims_above_50_yrs ,victims_of_rape_total  "
            query1 = query1 + "FROM victims_of_rape WHERE area_name = '"+state+"' ORDER BY year ASC, subgroup asc"
            print(query1)
            cursor.execute(query1)
            result1 = cursor.fetchall()


            # query2 = "SELECT year, sum(victims_upto_10_yr), sum(victims_between_10_14_yrs), sum(victims_between_14_18_yrs), sum(victims_between_18_30_yrs), sum(victims_between_30_50_yrs), sum(victims_above_50_yrs), sum(victims_of_rape_total) "
            # query2 += " FROM victims_of_rape WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC"
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, sum(victims_upto_10_yr), sum(victims_between_10_14_yrs), sum(victims_between_14_18_yrs), sum(victims_between_18_30_yrs), sum(victims_between_30_50_yrs), sum(victims_above_50_yrs), sum(victims_of_rape_total) "
            query2 += " FROM victims_of_rape WHERE area_name = '"+state+"' GROUP BY year ORDER BY year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(victims_upto_10_yr), sum(victims_between_10_14_yrs), sum(victims_between_14_18_yrs), sum(victims_between_18_30_yrs), sum(victims_between_30_50_yrs), sum(victims_above_50_yrs), sum(victims_of_rape_total) "
            query2 +=  " FROM victims_of_rape WHERE area_name = '"+state+"') as y "
            query2 += "ORDER BY year ASC"
            print("query2")
            print(query2)
            cursor.execute(query2)
            result2 = cursor.fetchall()
            year_val = [];
            t2_1 = [];
            t2_2 = [];
            t2_3 = [];
            t2_4 = [];
            t2_5 = [];
            t2_6 = [];
            t2_7 = [];

            for r in range(len(result2)-1):
                year_val.append(result2[r][0]);
                t2_1.append(result2[r][1]);
                t2_2.append(result2[r][2]);
                t2_3.append(result2[r][3]);
                t2_4.append(result2[r][4]);
                t2_5.append(result2[r][5]);
                t2_6.append(result2[r][6]);
                t2_7.append(result2[r][7]);

            query3 = "SELECT subgroup, sum(victims_upto_10_yr), sum(victims_between_10_14_yrs), sum(victims_between_14_18_yrs), sum(victims_between_18_30_yrs), sum(victims_between_30_50_yrs), sum(victims_above_50_yrs), sum(victims_of_rape_total) "
            query3 += "FROM victims_of_rape WHERE area_name = '"+state+"' GROUP BY subgroup ORDER BY subgroup ASC"
            cursor.execute(query3)
            result3 = cursor.fetchall()
            y_val = [];
            t3_1 = [];
            t3_2 = [];
            for r in result3:
                y_val.append(r[0]);
                t3_1.append(r[1]);
                t3_2.append(r[2]);
            




            x_data=[]
            # for year in year_types:
            #     x_data[year] = {}
            for (i,group) in enumerate(group_types):
                x_data.append([[],[],[],[],[],[],[]])
                for year in year_types:
                    query_temp = "SELECT COALESCE(victims_upto_10_yr,0),COALESCE(victims_between_10_14_yrs,0),COALESCE(victims_between_14_18_yrs,0),COALESCE(victims_between_18_30_yrs,0),COALESCE(victims_between_30_50_yrs,0),COALESCE(victims_above_50_yrs,0),COALESCE(victims_of_rape_total,0) FROM victims_of_rape WHERE subgroup='"+group+"' and year="+str(year)+" and area_name='"+state+"'"
                    cursor.execute(query_temp)
                    result_temp = cursor.fetchall()
                    print(result_temp)
                    if len(result_temp)==0:
                        x_data[i][0].append(0)
                        x_data[i][1].append(0)
                        x_data[i][2].append(0)
                        x_data[i][3].append(0)
                        x_data[i][4].append(0)
                        x_data[i][5].append(0)
                        x_data[i][6].append(0)
                        continue
                    x_data[i][0].append(result_temp[0][0])
                    x_data[i][1].append(result_temp[0][1])
                    x_data[i][2].append(result_temp[0][2])
                    x_data[i][3].append(result_temp[0][3])
                    x_data[i][4].append(result_temp[0][4])
                    x_data[i][5].append(result_temp[0][5])
                    x_data[i][6].append(result_temp[0][6])
            return render_template('rape_cases.html', state = state, result1 = result1,result2=result2, result3= result3,year_val=year_val,t2_1=t2_1,t2_2=t2_2,t2_3=t2_3,t2_4=t2_4,t2_5=t2_5,t2_6=t2_6,t2_7=t2_7,y_val=y_val,t3_1=t3_1,t3_2=t3_2,y_data=year_types, x_data=x_data, group_types=group_types) 

        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            query = "SELECT area_name, year, subgroup,victims_upto_10_yr, victims_between_10_14_yrs, victims_between_14_18_yrs,victims_between_18_30_yrs, victims_between_30_50_yrs, victims_above_50_yrs ,victims_of_rape_total  "
            query = query + "FROM victims_of_rape "
            if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                query += "WHERE "
            f=False
            g=False
            if not 'ALL' in compare_area:
                f=True
                query += " (area_name = '" + compare_area[0] + "'"
                for i in range(1, len(compare_area),1):
                    query += " OR area_name = '" + compare_area[i] +"'"
                query += " ) "
            if not 'ALL' in compare_year:
                if f:
                    query+=" AND "
                g=True
                query += "(year = " + compare_year[0]
                for i in range(1, len(compare_year),1):
                    query += " OR year = " + compare_year[i]
                query += " )"
            if not 'ALL' in compare_type:
                if f or g:
                    query+=" AND "
                query += "(subgroup = '" + compare_type[0] + "'"
                for i in range(1, len(compare_type),1):
                    query += " OR subgroup = '" + compare_type[i] + "'"
                query += " )"
            query += " ORDER BY area_name ASC, year ASC, subgroup ASC"
            print("query= "+ query)
            cursor.execute(query)
            result = cursor.fetchall()



            x_data_all = []
            for state_ in compare_area:
                x_data = []
                for (i,t) in enumerate(compare_type):
                    x_data.append([])
                    # print(i,type)
                    for year in compare_year:
                        query_temp = "SELECT COALESCE(victims_of_rape_total,0) FROM victims_of_rape WHERE subgroup='"+t+"' and year="+str(year)+" and area_name='"+state_+"'"
                        cursor.execute(query_temp)
                        result_temp = cursor.fetchall()
                        # print(result_temp, result[0][0])
                        if len(result_temp)==0:
                            x_data[i].append(0)
                            continue
                        # print(i, x_data)
                        x_data[i].append(result_temp[0][0])
                x_data_all.append(x_data)
            print(x_data_all)
            print(len(x_data_all))
            print(compare_type)
            print(compare_year)
            return render_template('rape_cases.html', compare_area = compare_area, compare_year=compare_year, compare_type = compare_type, result = result,types=compare_type, y_data=compare_year, x_data = x_data_all)
    else:
        return render_template('rape_cases.html')



# -----------------------------------------------  ADITYA CODE-------------



@app.route("/trial_of_violent_crimes2", methods=['POST', 'GET'])
def trial_of_violent_crimes2():
    table_name = "trial_of_violent_crimes_by_courts"
    state_list_query = f"select distinct area_name from {table_name} order by area_name;"
    cursor.execute(state_list_query)
    state_list = cursor.fetchall()
    # print(state_list)
    year_list_query = f"select distinct year from {table_name} order by year;"
    cursor.execute(year_list_query)
    year_list = cursor.fetchall()
    # print(year_list)
    type_list_query = f"select distinct sub_group_name from {table_name} order by sub_group_name;"
    cursor.execute(type_list_query)
    type_list = cursor.fetchall()
    # print(type_list)
    if request.method == 'POST':
        if "states" in request.form:
            state = request.form['states']
            print(state)
            view = "Create or replace View state_view as(Select year,sub_group_name," \
                   "trial_of_violent_crimes_by_courts_by_confession, trial_of_violent_crimes_by_courts_by_trial," \
                   "trial_of_violent_crimes_by_courts_total from trial_of_violent_crimes_by_courts where " \
                   "area_name='Bihar' order by year, sub_group_name); "
            cursor.execute(view)
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, " \
                     "sum(trial_of_violent_crimes_by_courts_by_confession), " \
                     "sum(trial_of_violent_crimes_by_courts_by_trial), sum(trial_of_violent_crimes_by_courts_total) " \
                     "FROM trial_of_violent_crimes_by_courts WHERE area_name = '" + state + "' GROUP BY year ORDER BY " \
                                                                                            "year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(trial_of_violent_crimes_by_courts_by_confession), " \
                      "sum(trial_of_violent_crimes_by_courts_by_trial), sum(trial_of_violent_crimes_by_courts_total) " \
                      "FROM trial_of_violent_crimes_by_courts WHERE area_name = '" + state + "') as y "
            query2 += "ORDER BY year ASC"
            cursor.execute(query2)
            result2 = cursor.fetchall()
            query3 = "SELECT sub_group_name, sum(trial_of_violent_crimes_by_courts_by_confession), " \
                     "sum(trial_of_violent_crimes_by_courts_by_trial), sum(trial_of_violent_crimes_by_courts_total) " \
                     "FROM trial_of_violent_crimes_by_courts WHERE area_name = '" + state + "' GROUP BY sub_group_name ORDER BY sub_group_name ASC "
            cursor.execute(query3)
            result3 = cursor.fetchall()
            chart_result2 = list()
            chart_result3 = list()
            for i in range(0, 4):
                out = [t[i] for t in result2]
                out2 = [t[i] for t in result3]
                chart_result2.append(out)
                chart_result3.append(out2)
            compare_crimes = request.form.getlist('compare_crimes')
            print(compare_crimes)
            print_queries = list()
            output1 = list()
            query_group_list = compare_crimes
            query_group_list_len = len(query_group_list)
            for x in compare_crimes:
                temp_query = f"SELECT year, {table_name}_by_confession,{table_name}_by_trial,{table_name}_total from state_view where sub_group_name = '{x}' order by year asc; "
                cursor.execute(temp_query)
                out = cursor.fetchall()
                out1 = list()
                for i in range(0, 4):
                    out1.append([t[i] for t in out])
                print_queries.append(out)
                output1.append(out1)
            # print(print_queries)
            years = [t[0] for t in print_queries[0]]
            # print(years)
            chart_names = ['Chart'+repr(i) for i in range(1,query_group_list_len+1)]
            print(chart_names)
            return render_template('trial_of_violent_crimes2.html', state=state, result2=result2,
                                   result3=result3, state_list=state_list, year_list=year_list, type_list=type_list,
                                   print_queries=print_queries,query_group_list=query_group_list,
                                   query_group_list_len=query_group_list_len,years=years,output1=output1,
                                   chart_names=chart_names, chart_result2=chart_result2,chart_result3=chart_result3)
        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            print_queries2 = list()
            output2 = list()
            query_state_list = compare_area
            query_state_list_len = len(query_state_list)
            for x in compare_area:
                query = f"SELECT year,{table_name}_by_confession, {table_name}_by_trial, {table_name}_total FROM {table_name} "
                if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                    query += "WHERE "
                f = False
                g = False
                if not 'ALL' in compare_area:
                    f = True
                    query += f" area_name = '{x}'"
                if not 'ALL' in compare_year:
                    if f:
                        query += " AND "
                    g = True
                    query += "(year = " + compare_year[0]
                    for i in range(1, len(compare_year), 1):
                        query += " OR year = " + compare_year[i]
                    query += " )"
                if not 'ALL' in compare_type:
                    if f or g:
                        query += " AND "
                    query += "(sub_group_Name = '" + compare_type[0] + "'"
                    for i in range(1, len(compare_type), 1):
                        query += " OR sub_group_Name = '" + compare_type[i] + "'"
                    query += " )"
                query += " ORDER BY area_name ASC, year ASC, sub_group_name ASC"
                print(query)
                cursor.execute(query)
                out = cursor.fetchall()
                print_queries2.append(out)
                out2 = list()
                for i in range(0, 4):
                    out2.append([t[i] for t in out])
                output2.append(out2)
            years = [t[0] for t in print_queries2[0]]
            print(years)
            chart_names2 = ['Chart2' + repr(i) for i in range(1, query_state_list_len + 1)]
                # print(print_queries2)
            return render_template('trial_of_violent_crimes2.html', compare_area=compare_area,
                                   compare_year=compare_year, compare_type=compare_type,
                                   state_list=state_list, year_list=year_list, type_list=type_list,
                                   print_queries2=print_queries2,query_state_list=query_state_list,
                                   query_state_list_len=query_state_list_len,output2=output2,
                                   years=years, chart_names2=chart_names2)
    elif request.method == 'GET':
        print("GET")
        return render_template('trial_of_violent_crimes2.html', state_list=state_list, year_list=year_list,
                               type_list=type_list)
    else:
        print("ELSE")
        print(repr(request.method))
        return "Error in HTTP request"


@app.route("/period_of_trials2", methods=['POST', 'GET'])
def period_of_trials2():
    table_name = "period_of_trials_by_courts"
    state_list_query = f"select distinct area_name from {table_name} order by area_name;"
    cursor.execute(state_list_query)
    state_list = cursor.fetchall()
    # print(state_list)
    year_list_query = f"select distinct year from {table_name} order by year;"
    cursor.execute(year_list_query)
    year_list = cursor.fetchall()
    # print(year_list)
    type_list_query = f"select distinct sub_group_name from {table_name} order by sub_group_name;"
    cursor.execute(type_list_query)
    type_list = cursor.fetchall()
    # print(type_list)
    if request.method == 'POST':
        if "states" in request.form:
            state = request.form['states']
            print(state)
            view = "Create or replace View state_view_2 as(SELECT year, sub_group_name, pt_less_than_6_months + " \
                   "pt_6_12_months as pt_less_than_1_year," \
                   "pt_1_3_years + pt_3_5_years as pt_1_5_years,pt_5_10_years,pt_over_10_years, pt_total FROM " \
                   "period_of_trials_by_courts WHERE area_name = '" + state + "' ORDER BY year ASC, sub_group_name ASC );"
            cursor.execute(view)
            query2 = "SELECT * FROM(SELECT CAST(@year as varchar(10)) as year, " \
                     "sum(pt_less_than_6_months) + sum(pt_6_12_months) as pt_less_than_1_year, sum(pt_1_3_years) + " \
                     "sum(pt_3_5_years) as pt_1_5_years, " \
                     "sum(pt_5_10_years), sum(pt_over_10_years), sum(pt_total)" \
                     "FROM period_of_trials_by_courts WHERE area_name = '" + state + "' GROUP BY year ORDER BY " \
                                                                                     "year ASC) as x "
            query2 += "UNION "
            query2 += "SELECT * FROM(SELECT 'Total' AS year, sum(pt_less_than_6_months) + sum(pt_6_12_months) as " \
                      "pt_less_than_1_year, " \
                      "sum(pt_1_3_years) + sum(pt_3_5_years) as pt_1_5_years , sum(pt_5_10_years), " \
                      "sum(pt_over_10_years), sum(pt_total)" \
                      "FROM period_of_trials_by_courts WHERE area_name = '" + state + "') as y "
            query2 += "ORDER BY year ASC"
            cursor.execute(query2)
            result2 = cursor.fetchall()
            query3 = "SELECT sub_group_name," \
                     "sum(pt_less_than_6_months) + sum(pt_6_12_months) as pt_less_than_1_year , sum(pt_1_3_years)+ " \
                     "sum(pt_3_5_years) as pt_1_5_years, " \
                     "sum(pt_5_10_years), sum(pt_over_10_years), sum(pt_total)" \
                     "FROM period_of_trials_by_courts WHERE area_name = '" + state + "' GROUP BY sub_group_name ORDER " \
                                                                                     "BY sub_group_name ASC "
            cursor.execute(query3)
            result3 = cursor.fetchall()
            chart_result2 = list()
            chart_result3 = list()
            for i in range(0,6):
                out = [t[i] for t in result2]
                out2 = [t[i] for t in result3]
                chart_result2.append(out)
                chart_result3.append(out2)
            compare_crimes = request.form.getlist('compare_crimes')
            print(compare_crimes)
            print_queries = list()
            output1 = list()
            query_group_list = compare_crimes
            query_group_list_len = len(query_group_list)
            for x in compare_crimes:
                temp_query = f"SELECT year, pt_less_than_1_year, pt_1_5_years, pt_5_10_years, " \
                             f"pt_over_10_years, pt_total from state_view_2  where sub_group_name = '{x}' order by " \
                             f"year asc; "
                cursor.execute(temp_query)
                out = cursor.fetchall()
                out1 = list()
                for i in range(0, 6):
                    out1.append([t[i] for t in out])
                print_queries.append(out)
                output1.append(out1)
                print_queries.append(out)
            print(len(output1[0]))
            years = [t[0] for t in print_queries[0]]
            chart_names = ['Chart' + repr(i) for i in range(1, query_group_list_len + 1)]
            print(chart_names)
            return render_template('period_of_trials2.html', state=state, result2=result2,
                                   result3=result3, state_list=state_list, year_list=year_list, type_list=type_list,
                                   print_queries=print_queries, query_group_list=query_group_list,
                                   query_group_list_len=query_group_list_len,years=years,output1=output1,chart_names=chart_names,
                                   chart_result2=chart_result2,chart_result3=chart_result3)
        else:
            compare_area = request.form.getlist('compare_area')
            compare_year = request.form.getlist('compare_year')
            compare_type = request.form.getlist('compare_type')
            print(compare_area)
            print(compare_year)
            print(compare_type)
            print_queries2 = list()
            output2 = list()
            query_state_list = compare_area
            query_state_list_len = len(query_state_list)
            for x in compare_area:
                query = "SELECT year,pt_less_than_6_months + pt_6_12_months as " \
                        "pt_less_than_1_year, pt_1_3_years + pt_3_5_years as pt_1_5_years, pt_5_10_years, " \
                        "pt_over_10_years, pt_total FROM period_of_trials_by_courts"
                if not ('ALL' in compare_area and 'ALL' in compare_type and 'ALL' in compare_year):
                    query += " WHERE "
                f = False
                g = False
                if not 'ALL' in compare_area:
                    f = True
                    query += f" area_name = '{x}'"
                if not 'ALL' in compare_year:
                    if f:
                        query += " AND "
                    g = True
                    query += "(year = " + compare_year[0]
                    for i in range(1, len(compare_year), 1):
                        query += " OR year = " + compare_year[i]
                    query += " )"
                if not 'ALL' in compare_type:
                    if f or g:
                        query += " AND "
                    query += "(sub_group_Name = '" + compare_type[0] + "'"
                    for i in range(1, len(compare_type), 1):
                        query += " OR sub_group_Name = '" + compare_type[i] + "'"
                    query += " )"
                query += " ORDER BY area_name ASC, year ASC, sub_group_name ASC"
                print(query)
                cursor.execute(query)
                out = cursor.fetchall()
                out2 = list()
                for i in range(0, 6):
                    out2.append([t[i] for t in out])
                output2.append(out2)
                print_queries2.append(out)
            print(print_queries2)
            years = [t[0] for t in print_queries2[0]]
            print(years)
            chart_names2 = ['Chart2' + repr(i) for i in range(1, query_state_list_len + 1)]
            return render_template('period_of_trials2.html', compare_area=compare_area,
                                   compare_year=compare_year, compare_type=compare_type,
                                   state_list=state_list, year_list=year_list, type_list=type_list,
                                   print_queries2=print_queries2, query_state_list=query_state_list,
                                   query_state_list_len=query_state_list_len,output2=output2,
                                   years=years, chart_names2=chart_names2)
    elif request.method == 'GET':
        print("GET")
        return render_template('period_of_trials2.html', state_list=state_list, year_list=year_list,
                               type_list=type_list)



if __name__ == '__main__':
    app.run(port=5012,debug=True)
    