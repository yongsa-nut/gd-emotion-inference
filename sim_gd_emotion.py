'''
Created on Apr 23, 2017

@author: nutjung
'''
import math
import random

def normalize(d):
    total = 0.0
    for i in d:
        total+=d[i]
    for i in d:
        d[i] = d[i]/total
    return d

# P(X|D,E) 
def genDisplayTable(list_au, list_dis, list_emo):
    
    ## default probability distribution
    # None, Low, High
    none_prob_dist = {"None":0.95,"Low":0.04,"High":0.01}
    low_prob_dist = {"None":0.60,"Low":0.35,"High":0.05}
    mid_prob_dist = {"None":0.05,"Low":0.60,"High":0.35}
    high_prob_dist = {"None":0.05,"Low":0.35,"High":0.60}
    max_prob_dist = {"None":0.01,"Low":0.04,"High":0.95} 
    
    
    dis_dict = {}
    for i in list_emo:
        dis_dict[i] = {}
        for j in list_dis:
            dis_dict[i][j] = {}
            for k in list_au:
                dis_dict[i][j][k] = none_prob_dist
    
    #####   Happy  #####
    
    ## Low Display ##
    dis_dict["Hl"]["L"][6] = low_prob_dist
    dis_dict["Hh"]["L"][6] = mid_prob_dist
    dis_dict["Hl"]["L"][12] = mid_prob_dist
    dis_dict["Hh"]["L"][12] = high_prob_dist
    ## High Display ##
    dis_dict["Hl"]["H"][6] = mid_prob_dist
    dis_dict["Hh"]["H"][6] = high_prob_dist
    dis_dict["Hl"]["H"][12] = high_prob_dist
    dis_dict["Hh"]["H"][12] = max_prob_dist
    ## Out Display ##
    dis_dict["Hl"]["O"][6] = low_prob_dist
    dis_dict["Hh"]["O"][6] = mid_prob_dist
    dis_dict["Hl"]["O"][12] = low_prob_dist
    dis_dict["Hh"]["O"][12] = mid_prob_dist
    dis_dict["Hl"]["O"][23] = low_prob_dist 
    dis_dict["Hh"]["O"][23] = mid_prob_dist
    
    
    #####   Sad   #####
    
    ## Low Display ##
    dis_dict["Sl"]["L"][1] = mid_prob_dist
    dis_dict["Sh"]["L"][1] = high_prob_dist
    dis_dict["Sl"]["L"][4] = low_prob_dist
    dis_dict["Sh"]["L"][4] = mid_prob_dist
    dis_dict["Sl"]["L"][15] = low_prob_dist
    dis_dict["Sh"]["L"][15] = mid_prob_dist
    
    ## High Display ##
    dis_dict["Sl"]["H"][1] = high_prob_dist
    dis_dict["Sh"]["H"][1] = max_prob_dist
    dis_dict["Sl"]["H"][4] = mid_prob_dist
    dis_dict["Sh"]["H"][4] = high_prob_dist
    dis_dict["Sl"]["H"][15] = mid_prob_dist
    dis_dict["Sh"]["H"][15] = high_prob_dist
    
    ## Out Display ##
    dis_dict["Sl"]["O"][1] = low_prob_dist
    dis_dict["Sh"]["O"][1] = mid_prob_dist
    dis_dict["Sl"]["O"][4] = low_prob_dist
    dis_dict["Sh"]["O"][4] = mid_prob_dist
    dis_dict["Sl"]["O"][12] = low_prob_dist
    dis_dict["Sh"]["O"][12] = mid_prob_dist
    
    #####   Angry    #####
    
    ## Low Display ##
    dis_dict["Al"]["L"][4] = low_prob_dist
    dis_dict["Ah"]["L"][4] = mid_prob_dist
    dis_dict["Al"]["L"][5] = mid_prob_dist
    dis_dict["Ah"]["L"][5] = high_prob_dist
    dis_dict["Al"]["L"][23] = low_prob_dist
    dis_dict["Ah"]["L"][23] = mid_prob_dist
    
    ## High Display ##
    dis_dict["Al"]["H"][4] = mid_prob_dist
    dis_dict["Ah"]["H"][4] = high_prob_dist
    dis_dict["Al"]["H"][5] = high_prob_dist
    dis_dict["Ah"]["H"][5] = max_prob_dist
    dis_dict["Al"]["H"][23] = mid_prob_dist
    dis_dict["Ah"]["H"][23] = high_prob_dist
    
    ## Out Display ##
    dis_dict["Al"]["O"][4] = low_prob_dist
    dis_dict["Ah"]["O"][4] = mid_prob_dist
    dis_dict["Al"]["O"][5] = mid_prob_dist
    dis_dict["Ah"]["O"][5] = high_prob_dist
    dis_dict["Al"]["O"][12] = mid_prob_dist
    dis_dict["Ah"]["O"][12] = low_prob_dist
    
    #####   No Emotion   #####
    
    ## Low Display ##
    #all low
    
    ## High Display ##
    #like to smile as default
    dis_dict["N"]["H"][12] = low_prob_dist
    
    ## Out Display ##
    dis_dict["N"]["O"][15] = low_prob_dist
    
    return dis_dict

def print_dis_dict(dis_dict):
    for i in dis_dict:
        print i
        for j in dis_dict[i]:
            print j
            print dis_dict[i][j]

def logistic(x,x0,L,k):
    return L/(1.0 + math.exp(-k*(x-x0)))

def utility(outcome, expectation):
    k = 0.15
    L = 2.0
    return logistic(outcome, expectation, L, k) - 1.0

def probPlease(outcome, expectation):
    p = {"Ph":0.0,"Pl":0.0,"N":0.0,"DPl":0.0,"DPh":0.0}
    ut = utility(outcome, expectation)

    if ut <= 1.0 and ut >=0.5:
        #print "First Condi"
        slope = -2
        c = 2
        temp_p = ut*slope + c 
        
        p["Pl"] = temp_p 
        p["Ph"] = 1-temp_p
    elif ut < 0.5 and ut >= 0.0:
        #print "Second Condi"
        slope = 2.0
        c = 0 
        temp_p = ut*slope+c
        p["Pl"] = temp_p
        p["N"] = 1-temp_p
    elif ut < 0.0 and ut >= -0.5:
        #print "Third Condi"
        slope = -2
        c = 0
        temp_p = ut*slope +c
        p["DPl"] = temp_p
        p["N"] = 1-temp_p
    elif ut < -0.5 and ut >= -1.0:
        #print "Forth Condi"
        slope = 2
        c = 2
        temp_p = ut*slope + c
        p["DPl"] = temp_p
        p["DPh"] = 1-temp_p
    #p has to sum to 1, all pi >= 0 
    
    return p 

def EgivenGS(outcome,expectation,blame):
    pe = {"Hl":0.0,"Hh":0.0,"Sl":0.0,"Sh":0.0,"Al":0.0,"Ah":0.0,"N":0.0}
    please_p = probPlease(outcome,expectation)
    pe["Hl"] = please_p["Pl"]
    pe["Hh"] = please_p["Ph"]
    pe["N"] = please_p["N"]
    pe["Sl"] = please_p["DPl"]*blame["event"]
    pe["Sh"] = please_p["DPh"]*blame["event"]
    pe["Al"] = please_p["DPl"]*blame["agent"]
    pe["Ah"] = please_p["DPh"]*blame["agent"]
    return pe

#p(g,s,d,e,X) = p(s)p(g)p(d)p(e|s,g)p(X|d,e)
def jointDistibution(g,pg,d,pd,e,s,X,dis_table):
    p_E = EgivenGS(s, g["expectation"], g["blame"])
    p_X = 1.0
    for x in X:
        p_X = p_X*dis_table[e][d][x][X[x]]
    
    return pg*pd*p_E[e]*p_X

# P(E|s,X) = Sum{g,d} P(E,s,X,g,d)/P(s,x)
def infer_emotion(s,X,G,G_ref,D,dis_table):
    list_emo = ["Hl","Hh","Sl","Sh","Al","Ah","N"]
    p_e = {}
    for e in list_emo:
        total = 0.0
        for g in G:
            for d in D:
                total += jointDistibution(G_ref[g], G[g], d, D[d], e, s, X, dis_table)
        p_e[e] = total
    return normalize(p_e)

# P(G|s,X) = sum{e,d} P(E,s,X,G,d)/P(s,X)
def update_G(G,G_ref,D,s,X, dis_table):
    list_emo = ["Hl","Hh","Sl","Sh","Al","Ah","N"]
    p_g = {}
    for g in G:
        total = 0.0
        for e in list_emo:
            for d in D:
                total += jointDistibution(G_ref[g], G[g], d, D[d], e, s, X, dis_table)
        p_g[g] = total
    return normalize(p_g)

# P(D|s,X) = sum{e,g} P(E,s,X,G,d)/P(s,X)
def update_D(G,G_ref,D,s,X, dis_table):
    list_emo = ["Hl","Hh","Sl","Sh","Al","Ah","N"]
    p_d = {}
    for d in D:
        total = 0.0
        for e in list_emo:
            for g in G:
                total += jointDistibution(G_ref[g], G[g], d, D[d], e, s, X, dis_table)
        p_d[d] = total
    return normalize(p_d)

def rand_from_dict(dic):
    r = random.random()
    total = 0.0
    for d in dic:
        total += dic[d]
        if r < total:
            return d
    return 

def max_prob_dist(p_dist):
    max_p = 0.0
    max_key = None
    for d in p_dist:
        if p_dist[d] > max_p:
            max_p = p_dist[d]
            max_key = d
    return max_key

#Given situation, gen E and X
def genData(s,g_true,d_true,dis_table):
    p_E = EgivenGS(s, g_true["expectation"], g_true["blame"])
    e_true = max_prob_dist(p_E)
    #gen dict of AU
    X = {}
    list_au = [1,4,5,6,12,15,23]
    for au in list_au:
        X[au] = rand_from_dict(dis_table[e_true][d_true][au])
    return e_true, X

#return error of prediction at each observation {0,1}
#return p of d_true, p of g_true
def simulation(D,G,G_ref,d_true,g_true,dis_table,num_observation):
    error_e = []
    p_d_true = []
    p_g_true = []
    for t in range(num_observation):
        #gen situation
        s = random.randint(0,100)
        #gen emotion, expression
        e_true, X = genData(s, G_ref[g_true], d_true, dis_table)
        #print e_true, X
        
        #make prediciton
        e_predict = infer_emotion(s, X, G, G_ref, D, dis_table)
        #print s, e_predict
        e_predict = max_prob_dist(e_predict)
        #print e_predict, e_true
        
        #update 
        G = update_G(G, G_ref, D, s, X, dis_table)
        D = update_D(G, G_ref, D, s, X, dis_table)
        
        error_e.append(e_true==e_predict)
        p_d_true.append(D[d_true])
        p_g_true.append(G[g_true])
        
    return error_e, p_d_true, p_g_true
    

if __name__ == '__main__':
    
    #param setting 
    
    list_au = [1,4,5,6,12,15,23]
    list_emo = ["Hl","Hh","Sl","Sh","Al","Ah","N"]
    list_dis = ["L","H","O"]
    
    
    dis_table = genDisplayTable(list_au, list_dis, list_emo)
    
    #print_dis_dict(dis_dict)
    
    num_expect = 3  # L = 25, M = 50, H = 75
    num_blame = 2   # Likely = {A:.8, E:.2}, Unlikely = {A:.2, E:.8}
    num_goal = num_expect * num_blame  
    
    num_iteration = 100
    num_observation = 50
    
    
    blamelikely = {"agent":0.8,"event":0.2}
    blameunlikely = {"agent":0.2, "event":0.8}
    g1 = {"expectation":25,"blame":blamelikely}
    g2 = {"expectation":25,"blame":blameunlikely}
    g3 = {"expectation":50,"blame":blamelikely}
    g4 = {"expectation":50,"blame":blameunlikely}
    g5 = {"expectation":75,"blame":blamelikely}
    g6 = {"expectation":75,"blame":blameunlikely}
    
    G_ref = {"g1":g1,"g2":g2,"g3":g3,"g4":g4,"g5":g5,"g6":g6} 
    
    
    ##### experiment below #####
    f = open("output.txt","w")
    
    for d in list_dis:
        for g in G_ref:
            print d,g
            total_e = [0.0]*num_observation
            total_p_g_true = [0.0]*num_observation
            total_p_d_true = [0.0]*num_observation
            for iteration in range(num_iteration):
                print iteration+1
                random.seed(iteration+1)
                D = {"L":0.33,"H":0.34,"O":0.33}
                G = {"g1":0.166,"g2":0.166,"g3":0.17,"g4":0.166,"g5":0.166,"g6":0.166}
                error_e, p_d_true, p_g_true = simulation(D, G, G_ref, d, g, dis_table, num_observation)
                #sum error/p
                for k in range(num_observation):
                    total_e[k] += error_e[k]
                    total_p_d_true[k] += p_d_true[k]
                    total_p_g_true[k] += p_g_true[k]
            #print the avg of error/p
            for k in range(num_observation):
                total_e[k]= total_e[k]/num_iteration
                total_p_d_true[k] = total_p_d_true[k]/num_iteration
                total_p_g_true[k] = total_p_g_true[k]/num_iteration
            
            print >>f, d , g
            print >>f, "Error Output"
            for k in range(num_observation):
                print >>f, total_e[k]
            print >>f, "Display Output"
            for k in range(num_observation):
                print >>f, total_p_d_true[k]
            print >>f, "Goal Output"
            for k in range(num_observation):
                print >>f, total_p_g_true[k]
    
    f.close()
    