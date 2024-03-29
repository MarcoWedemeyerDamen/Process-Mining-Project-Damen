from neo4j import GraphDatabase
from graphviz import Digraph
import graphviz
from datetime import datetime
import numpy as np
import os
import pandas as pd


### begin config
# connection to Neo4J database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234"))

# Crimson 
c1 =  "#DC143C" 
# HotPink  
c2 = "#FF69B4"
# DeepPink 
c3 = "#FF1493"
# Pink 
c4 = "#FFC0CB"
# MediumVioletRed 
c5 = "#C71585"
# Orchid 
c6 = "#DA70D6"
# Thistle 
c7 = "#D8BFD8"
# plum 
c8 = "#DDA0DD"
# Violet 
c9 = "#EE82EE"
# Magenta 
c10 = "#FF00FF"
# Fuchsia 
c11 = "#FF00FF"
# DarkMagenta 
c12 = "#8B008B"
# Purple 
c13 = "#800080"
# MediumOrchid 
c14 = "#BA55D3"
# DarkVoilet 
c15 = "#9400D3"
# DarkOrchid 
c16 = "#9932CC"
# Indigo 
c17 = "#4B0082"
# BlueViolet 
c18 = "#8A2BE2"
# RosyBrown
c19 = "#BC8F8F"
# IndianRed
c20 = "#CD5C5C"
# Red
c21 = "#FF0000"
# Brown
c22 = "#A52A2A"
# FireBrick
c23 = "#B22222"
# DarkRed
c24 = "#8B0000"



c2_cyan = "#318599"
c2_orange = "#ea700d"
c2_light_orange = "#f59d56"
c2_light_yellow = "#ffd965"

c3_light_blue = "#5b9bd5"
c3_red = "#ff0000"
c3_green = "#70ad47"
c3_yellow = "#ffc000"

c4_red = '#d7191c'
c4_orange = '#fdae61'
c4_yellow = '#ffffbf'
c4_light_blue = '#abd9e9'
c4_dark_blue = '#2c7bb6'

c_white = "#ffffff"
c_black = "#000000"

c5_red = '#d73027'
c5_orange = '#fc8d59'
c5_yellow = '#fee090'
c5_light_blue = '#e0f3f8'
c5_medium_blue = '#91bfdb'
c5_dark_blue = '#4575b4'


# Baby Blue	
C1 = "#89CFF0"
# Blue	
C2 = "#0000FF"
# Blue Gray	
C3 = "#7393B3"
# Blue Green	
C4 = "#088F8F"
# Bright Blue	
C5 = "#0096FF"
# Cadet Blue	
C6 = "#5F9EA0"
# Cobalt Blue	
C7 = "#0047AB"
# Cornflower Blue	
C8 = "#6495ED"
# Cyan	
C9 = "#00FFFF"
# Dark Blue	
C10 = "#00008B"
# Denim	
C11 = "#6F8FAF"
# Egyptian Blue	
C12 = "#1434A4"
# Electric Blue	
C13 = "#7DF9FF"
# Glaucous	
C14 = "#6082B6"
# Jade	
C15 = "#00A36C"
# Indigo	
C16 = "#3F00FF"
# Iris	
C17 =  "#5D3FD3"
# Light Blue	
C18 = "#ADD8E6"
# Midnight Blue	
C19 = "#191970"
# Navy Blue	
C20 = "#000080"
# Neon Blue	
C21 = "#1F51FF"
# Pastel Blue	
C22 = "#A7C7E7"
# Periwinkle	
C23 = "#CCCCFF"
# Powder Blue	
C24 = "#B6D0E2"
# Robin Egg Blue	
C25 = "#96DED1"
# Royal Blue	
C26 = "#4169E1"
# Sapphire Blue	
C27 = "#0F52BA"
# Seafoam Green	
C28 = "#9FE2BF"



holidays = [
"2016-03-25",
"2016-05-16" ,
"2017-04-14" ,
"2017-04-27" ,
"2017-05-25" ,
"2018-03-30" ,
"2018-04-02" ,
"2018-04-27" ,
"2018-05-10" ,
"2018-05-21" ,
"2019-04-19" ,
"2019-05-30" ,
"2019-06-09" ,
"2019-06-10" ,
"2020-04-10" ,
"2020-04-27" ,
"2020-05-05" ,
"2020-06-01" ,
"2021-04-02" ,
"2021-04-05" ]

# all activities
AT_selector = 'True'


Projects = ['Project1','Project2','Project3','Project4','Project5','Project6','Project7','Project8','Project9','Project10']
Pro_selector = "e1.Project in "+str(Projects)
Pro_selector_e2 = "e2.Project in "+str(Projects)


def getEventsDF(tx, dot, ID, color, fontcolor, edge_width):
    q = f'''
        MATCH (n:Entity {{ID:"{ID}"}}) <-[:CORR]- (e1:Event) -[r:DF{{EntityType:'Project'}}]-> (e2:Event)
        WHERE {Pro_selector} AND {Pro_selector_e2}
        return e1,r,e2,n
        '''
    print(q)

    for record in tx.run(q):
        if record["e2"] != None:
            e1_id = str(record['e1'].id)
            e2_id = str(record['e2'].id)
            e1_date = str(record["e1"]["Date"])
            e1_name = str(record["e1"]["Date"])+ ' P'  + getNodeLabel_Event(str(record["e1"]["Project"]))+' '+ getNodeLabel_Event(str(record["e1"]["Person"]))
            e2_date = str(record["e2"]["Date"])
            e2_name = str(record["e2"]["Date"])+ ' P'  + getNodeLabel_Event(str(record["e2"]["Project"]))+' '+ getNodeLabel_Event(str(record["e2"]["Person"])) 
            e1_label = ' P'  + getNodeLabel_Event(str(record["e1"]["Project"]))+' '+ getNodeLabel_Event(str(record["e1"]["Person"]))
            e2_label = ' P'  + getNodeLabel_Event(str(record["e2"]["Project"]))+' '+ getNodeLabel_Event(str(record["e2"]["Person"]))                                                                                            
            e1_project = str(record['e1']['Project'])
            e2_project = str(record['e2']['Project'])
            days = np.busday_count(record['e1']['Date'], record['e2']['Date'], holidays = holidays)
            
            if e1_date == e2_date:
                edge_label = ""
                with dot.subgraph(name='cluster' + e1_date) as c:
                    c.node(e1_date)
                    with c.subgraph (name='cluster' + e1_date + e1_project) as a:
                        a.attr(style='filled', color= color)
                        a.node(e1_name,style='filled',fillcolor="white", fontcolor=fontcolor,label = e1_label)
                        a.node(e2_name,style='filled',fillcolor="white", fontcolor=fontcolor,label = e2_label)
                
                pen_width = str(edge_width)
                edge_color = color
                dot.edge(e1_name, e2_name,constraint = "false",color=edge_color,penwidth=pen_width,fontname="Helvetica", fontsize="8",fontcolor=edge_color) 
                                      
            else:
                if days == 0 or days ==1:
                    edge_label = "P" + record["e1"]["Project"][7:9]
                else:
                    edge_label = "P" + record["e1"]["Project"][7:9] +"__"+ str(int(days)-1) + ' days'
                with dot.subgraph(name='cluster' + e1_date) as c:
                    c.node(e1_date)
                    with c.subgraph (name='cluster' + e1_date + e1_project) as a:
                        a.attr(style='filled', color= color)
                        a.node(e1_name,style='filled',fillcolor="white", fontcolor=fontcolor,label = e1_label)
                with dot.subgraph(name='cluster' + e2_date) as c:
                    c.node(e2_date)
                    with c.subgraph (name='cluster' + e2_date + e2_project) as a:
                        a.attr(style='filled', color= color)
                        a.node(e2_name,style='filled',fillcolor="white", fontcolor=fontcolor,label = e2_label)
                pen_width = str(edge_width)
                edge_color = color
                dot.edge(e1_name, e2_name,constraint = "false",xlabel=edge_label,color=edge_color,penwidth=pen_width,fontname="Helvetica", fontsize="8",fontcolor=edge_color) 
                dot.attr(rankdir="LR")

def getResourcesDF(tx, dot, ID, color, fontcolor, edge_width):
    q = f'''
        match (n:Entity {{ID:"{ID}"}}) <-[:CORR]- (e1:Event) -[r:DF{{EntityType:'Person'}}]-> (e2:Event)
        WHERE {Pro_selector} AND {Pro_selector_e2}
        return e1,r,e2,n
        '''
    for record in tx.run(q):
        if record["e2"] != None:
            e1_date = str(record["e1"]["Date"])
            e1_name = str(record["e1"]["Date"])+ ' P'  + getNodeLabel_Event(str(record["e1"]["Project"]))+' '+ getNodeLabel_Event(str(record["e1"]["Person"]))
            e2_date = str(record["e2"]["Date"])
            e2_name = str(record["e2"]["Date"])+ ' P'  + getNodeLabel_Event(str(record["e2"]["Project"]))+' '+ getNodeLabel_Event(str(record["e2"]["Person"])) 
            e1_person = str(record['e1']['Person'])
            e2_person = str(record['e2']['Person'])
            e1_label = ' P'  + getNodeLabel_Event(str(record["e1"]["Project"]))+' '+ getNodeLabel_Event(str(record["e1"]["Person"]))
            e2_label = ' P'  + getNodeLabel_Event(str(record["e2"]["Project"]))+' '+ getNodeLabel_Event(str(record["e2"]["Person"]))                                                                                                      
            days = np.busday_count(record['e1']['Date'], record['e2']['Date'], holidays = holidays)
            if e1_date == e2_date:
                with dot.subgraph(name='cluster' + e1_date) as c:
                    c.node(e1_date)
                    c.node(e1_name,style='filled',fillcolor=color,label = e1_label,fontcolor = fontcolor)
                    c.node(e2_name,style='filled',fillcolor=color,label = e2_label,fontcolor = fontcolor)
                dot.edge(e1_name,e2_name,constraint = "false",color = color)
            else: 
                with dot.subgraph(name='cluster' + e1_date) as c:
                    c.node(e1_date,fontcolor='black')
                    c.node(e1_name,style='filled',fillcolor=color, fontcolor=fontcolor,label = e1_label)
                with dot.subgraph(name='cluster' + e2_date) as c:
                    c.node(e2_date,fontcolor='black')
                    c.node(e2_name,style='filled',fillcolor=color, fontcolor=fontcolor,label = e2_label)
                if days == 0 or days == 1:
                    edge_label = "E"+ record["n"]["ID"][8:11]
                else:   
                    edge_label = "E"+ record["n"]["ID"][8:11] + "__"+str(int(days)-1) + ' days'
                pen_width = str(edge_width)
                dot.edge(e1_name,e2_name,constraint = "false",xlabel=edge_label,color=color,penwidth=pen_width,fontname="Helvetica", fontsize="8",fontcolor=color) 
                dot.attr(rankdir = "LR")
                
                

def getEntityForFirstEvent(tx,dot,ID,color,fontcolor):
    q = f'''
        MATCH (e1:Event) -[c:CORR]-> (n:Entity)
        WHERE n.ID = "{ID}" AND NOT (:Event)-[:DF{{EntityType:n.EntityType}}]->(e1) AND {Pro_selector}
        return e1,c,n
        '''
    print(q)
    for record in tx.run(q):
        
        e_date = str(record["e1"]['Date'])
        e_name = str(record["e1"]["Date"])+ ' P'  + getNodeLabel_Event(str(record["e1"]["Project"]))+' '+ getNodeLabel_Event(str(record["e1"]["Person"]))           
        entity_type = record["n"]["EntityType"]
        
        entity_id = record["n"]["ID"]
        entity_label = entity_type+'\n' +entity_id
        
        dot.node(entity_id, entity_label,shape="rectangle",color=color ,fixedsize="false", width="0.4", height="0.4", style="filled", fillcolor=color, fontcolor=fontcolor)
        dot.edge(entity_id, e_name, style="dashed", arrowhead="none",color=color)
        
         
                
 dot = Digraph("G",comment='Query Result')
dot.attr("graph",margin="0")

with driver.session() as session:
    session.read_transaction(getEventsDF, dot,"Project1" , c5_dark_blue, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project1",c5_dark_blue,c_white)
    
    session.read_transaction(getEventsDF, dot,"Project4" , c5_medium_blue, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project4",c5_medium_blue,c_white)  
    
    session.read_transaction(getEventsDF, dot,"Project2" , C1, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project2",C1,c_white)

    session.read_transaction(getEventsDF, dot,"Project3" , C3, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project3",C3,c_white)
    
    session.read_transaction(getEventsDF, dot,"Project5" , C4, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project5",C4,c_white)

    
    session.read_transaction(getEventsDF, dot,"Project6" , C6, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project6",C6,c_white)

    
    session.read_transaction(getEventsDF, dot,"Project7" , C8, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project7",C8,c_white)

    
    session.read_transaction(getEventsDF, dot,"Project8" , C11, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project8",C11,c_white)

    
    session.read_transaction(getEventsDF, dot,"Project9" , C14, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project9",C14,c_white)

    
    session.read_transaction(getEventsDF, dot,"Project10", C15, c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Project10",C15,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee55", c1, c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee55",c1,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee195", c2,c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee195",c2,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee161", c16,c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee161",c16,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee216", c3,c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee216",c3,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee1", c5, c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee1",c5,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee231", c6,c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee231",c6,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee256", c17,c_white, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee256",c17,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee23", c8,c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee23",c8,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee213", c9,c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee213",c9,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee78", c10, c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee78",c10,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee152", c11,c_black,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee152",c11,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee62", c12,c_white, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee62",c12,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee42", c13,c_white,3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee42",c13,c_white)
    
    session.read_transaction(getResourcesDF, dot, "Employee64", c14,c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee64",c14,c_white)

    session.read_transaction(getResourcesDF, dot, "Employee204", c15,c_black, 3)
    session.read_transaction(getEntityForFirstEvent, dot, "Employee204",c15,c_white)

    
    session.read_transaction(getActivityDF, dot)

    session.read_transaction(getEntityForFirstEvent, dot, "AT1",c5_orange,c_black)
     
file = open("activities.dot","w") 
file.write(dot.source)
file.close()
dot.render('test-output/round-table.gv', view=True)
               
                
                
                
           
