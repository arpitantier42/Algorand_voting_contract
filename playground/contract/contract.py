import beaker as bk
import pyteal as pt
from beaker.lib.storage import BoxMapping

class Proposal_Record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    proposal_name:pt.abi.Field[pt.abi.String]
    asset_count:pt.abi.Field[pt.abi.Uint64]
    Amount:pt.abi.Field[pt.abi.Uint64]

class Proposal_Record2(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    proposal_name:pt.abi.Field[pt.abi.String]
    asset_count:pt.abi.Field[pt.abi.Uint64]
    Amount:pt.abi.Field[pt.abi.Uint64]

class asset_store(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    asset_id:pt.abi.Field[pt.abi.String]

class User_per_proposal_record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    user_id:pt.abi.Field[pt.abi.String]
    
class User_asset_store(pt.abi.NamedTuple):
    user_id:pt.abi.Field[pt.abi.String]
    asset_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]
    
class Response_store(pt.abi.NamedTuple):
    user_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]
    user_response:pt.abi.Field[pt.abi.Uint64]
    question:pt.abi.Field[pt.abi.String]
  
class Question_store(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    question_id:pt.abi.Field[pt.abi.String]
    question_name:pt.abi.Field[pt.abi.String]

class option_store(pt.abi.NamedTuple):
    question_id:pt.abi.Field[pt.abi.String]
    option_1:pt.abi.Field[pt.abi.Uint64]
    option_2:pt.abi.Field[pt.abi.Uint64]
    option_3:pt.abi.Field[pt.abi.Uint64]
    option_4:pt.abi.Field[pt.abi.Uint64]
    option_5:pt.abi.Field[pt.abi.Uint64]
    option_6:pt.abi.Field[pt.abi.Uint64]
    option_7:pt.abi.Field[pt.abi.Uint64]

class Proposal_Record_State:
    proposal_rec = BoxMapping(pt.abi.String,Proposal_Record)
    proposal_rec2 = BoxMapping(pt.abi.String,Proposal_Record2,prefix=pt.Bytes("P"))
    user_rec = BoxMapping(pt.abi.String,User_per_proposal_record,prefix=pt.Bytes("_"))
    asset_rec = BoxMapping(pt.abi.String,User_asset_store,prefix=pt.Bytes("#"))
    response_rec = BoxMapping(pt.abi.String,Response_store,prefix=pt.Bytes("@"))
    asset_str = BoxMapping(pt.abi.String,asset_store,prefix=pt.Bytes("$"))
    question_rec = BoxMapping(pt.abi.String,Question_store,prefix=pt.Bytes("Q"))
    option_rec= BoxMapping(pt.abi.String,option_store,prefix=pt.Bytes("O"))

# --------------------------- Some Global Variable Declaration ----------------------------
    
    user_amount_chk = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    proposal_question_chk = bk.GlobalStateValue(
        stack_type=pt.TealType.bytes,
        default=pt.Bytes("0"),
    )

app =(
     bk.Application("Voting_Contract_fn_test",state = Proposal_Record_State())
     .apply(bk.unconditional_create_approval,initialize_global_state=True)
     )
 
# ---------------------------- Function to Register Proposal -----------------------------

@app.external
def Register_proposal(proposal_id:pt.abi.String, proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,Amount:pt.abi.Uint64,* ,output:Proposal_Record) -> pt.Expr:

    proposal_store = Proposal_Record()
    proposal_store2 = Proposal_Record2()

    return pt.Seq(

    app.state.user_amount_chk.set(pt.Int(0)),
    proposal_store.set(proposal_id,proposal_name,asset_count,Amount),
    pt.Assert(app.state.proposal_rec[proposal_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),
    app.state.proposal_rec[proposal_id.get()].set(proposal_store),
    app.state.proposal_rec[proposal_id.get()].store_into(output),

    proposal_store2.set(proposal_id,proposal_name,asset_count,Amount),
    app.state.proposal_rec2[proposal_id.get()].set(proposal_store2),

    ) 
 
#------------------------- Function to Register Multiple Questions ------------------------

@app.external
def RegisterQues(proposal_id:pt.abi.String,question_id:pt.abi.String,question:pt.abi.String,* ,output:Question_store)->pt.Expr:

    proposal_get = Proposal_Record()
    question_store1=Question_store()
    option_get=option_store()

    return pt.Seq(
    
    app.state.proposal_question_chk.set(pt.Bytes("0")),
    # //options
    (option_1 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_2 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_3 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_4 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_5 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_6 :=pt.abi.Uint64()).set(pt.Int(0)),
    (option_7 :=pt.abi.Uint64()).set(pt.Int(0)),

    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
    question_store1.set(proposal_id,question_id,question),
    pt.Assert(app.state.question_rec[question_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),
    
    app.state.proposal_question_chk.set(question_id.get()),
    app.state.question_rec[question_id.get()].set(question_store1),
    app.state.question_rec[question_id.get()].store_into(output),
    option_get.set(question_id,option_1,option_2,option_3,option_4,option_5,option_6,option_7),
    app.state.option_rec[question_id.get()].set(option_get),
    )
 
#----------------------------- Function to Register User Per Proposal ------------------------------

@app.external
def Registred_user_per_proposal(proposal_id:pt.abi.String,user_id:pt.abi.String,*,output:User_per_proposal_record)-> pt.Expr:

    registred_user = User_per_proposal_record()
    proposal_get = Proposal_Record()
    
    return pt.Seq(
    
    registred_user.set(proposal_id,user_id),
    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
       
    pt.Assert(app.state.user_rec[user_id.get()].exists()==pt.Int(0),comment="User_ID already exists"),
    app.state.user_rec[(user_id).get()].set(registred_user),
    app.state.user_rec[user_id.get()].store_into(output),
    ) 
                                                                        
#------------------------------ Function to Register Assets in the Proposal --------------------------------

@app.external
def asset_register(proposal_id:pt.abi.String,asset_id:pt.abi.String,*,output:asset_store)->pt.Expr:
    
    proposal_get = Proposal_Record()
    asset_get = asset_store()

    return pt.Seq(
    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
    asset_get.set(proposal_id,asset_id),
    pt.Assert(app.state.asset_str[asset_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),

    app.state.asset_str[asset_id.get()].set(asset_get),
    app.state.asset_str[asset_id.get()].store_into(output),
    )      
    
#-------------------------------- Function to Register User Per Asset -------------------------------

@app.external
def Register_user_asset(proposal_id:pt.abi.String,user_id:pt.abi.String,
     asset_id:pt.abi.String,token_count:pt.abi.Uint64,*,output:pt.abi.String)-> pt.Expr:
    
    asset_register = User_asset_store()
    registred_user = User_per_proposal_record()
    existing_proposal_store = Proposal_Record()
    asset_get = asset_store()
    
    return pt.Seq(
        
    existing_proposal_store.decode(app.state.proposal_rec[proposal_id.get()].get()),
    (proposal_asset_count :=pt.abi.make(pt.abi.Uint64)).set(existing_proposal_store.asset_count),
    (proposal_name :=pt.abi.make(pt.abi.String)).set(existing_proposal_store.proposal_name),
    (proposal_Amount :=pt.abi.make(pt.abi.Uint64)).set(existing_proposal_store.Amount),

    pt.Assert(proposal_asset_count.get()>=token_count.get()),
    
    registred_user.decode(app.state.user_rec[user_id.get()].get()),
    asset_get.decode(app.state.asset_str[asset_id.get()].get()),
 
    pt.If(app.state.asset_rec[user_id.get()].exists()== pt.Int(0)).Then(
    asset_register.set(user_id,asset_id,token_count),
    app.state.asset_rec[(user_id).get()].set(asset_register),

    proposal_asset_count.set(proposal_asset_count.get()-token_count.get()),
    existing_proposal_store.set(proposal_id,proposal_name,proposal_asset_count,proposal_Amount),
    app.state.proposal_rec[proposal_id.get()].set(existing_proposal_store),

    app.state.asset_rec[user_id.get()].store_into(output),

    ).Else(
    asset_register.decode(app.state.asset_rec[user_id.get()].get()),
    (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_register.asset_id),

    pt.Assert(asset_id.get()!=user_asset_store.get()),
    (token_count_update :=pt.abi.make(pt.abi.Uint64)).set(asset_register.User_Token),
    token_count_update.set(token_count_update.get()+token_count.get()),
    asset_register.set(user_id,asset_id,token_count_update),
    app.state.asset_rec[(user_id).get()].set(asset_register),

    proposal_asset_count.set(proposal_asset_count.get()-token_count.get()),
    existing_proposal_store.set(proposal_id,proposal_name,proposal_asset_count,proposal_Amount),
    app.state.proposal_rec[proposal_id.get()].set(existing_proposal_store),

    app.state.asset_rec[user_id.get()].store_into(output), 
    ),
    )

#------------------------- Function for "Voting for Question in a Proposal" ----------------------

@app.external
def Voting_Record(proposal_id:pt.abi.String,user_id:pt.abi.String,
                  token_count:pt.abi.Uint64,question_id:pt.abi.String,
                  user_response:pt.abi.Uint64,*,output:Response_store)-> pt.Expr:
     
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    asset_store = User_asset_store()
    response_get = Response_store()
    option_get=option_store()

    return pt.Seq(
    pt.Assert(app.state.proposal_question_chk==question_id.get()),
    pt.Assert(user_response.get()<=pt.Int(7)),
    pt.Assert(user_response.get()>=pt.Int(1)),

    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
    user_store.decode(app.state.user_rec[user_id.get()].get()),
   (user_store1 :=pt.abi.make(pt.abi.String)).set(user_store.proposal_id),
    pt.Assert(user_store1.get()==proposal_id.get()),

    asset_store.decode(app.state.asset_rec[user_id.get()].get()),
    pt.If(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].exists()== pt.Int(0)).Then(
   
    (concat:=pt.abi.String()).set(pt.Concat(question_id.get(),user_id.get())),
    response_get.set(concat,token_count,user_response,question_id),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].set(response_get),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].store_into(output),

    ).Else(
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),

    (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),
    pt.Assert(question_id.get()!=user_question_store.get()),
    (concat:=pt.abi.String()).set(pt.Concat(question_id.get(),user_id.get())),
    response_get.set(concat,token_count,user_response,question_id),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].set(response_get),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].store_into(output),

    ),

    asset_store.decode(app.state.asset_rec[user_id.get()].get()),
    (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),

    pt.Assert(user_token_store.get()==token_count.get()),
#    //// 

     option_get.decode(app.state.option_rec[question_id.get()].get()),
    (option_1_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_1),
    (option_2_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_2),
    (option_3_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_3),
    (option_4_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_4),
    (option_5_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_5),
    (option_6_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_6),
    (option_7_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_7),

  
    pt.If (user_response.get() == pt.Int(1)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_1_store.set(option_1_store.get()+ token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(2)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_2_store.set(option_2_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(3)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_3_store.set(option_3_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(4)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_4_store.set(option_4_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(5)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_5_store.set(option_5_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(6)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_6_store.set(option_6_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ).ElseIf(

    user_response.get() == pt.Int(7)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_7_store.set(option_7_store.get()+token_count.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),
    ),
    )    

#------------------------- Function to Buy Tokens in Secondary Market Place ------------------------

@app.external
def token_buy(proposal_id:pt.abi.String,
              user_id:pt.abi.String,question_id:pt.abi.String,user_response:pt.abi.Uint64,
              token_buy:pt.abi.Uint64)->pt.Expr:
                 
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    question_store1 = Question_store()
    response_get = Response_store()
    asset_store = User_asset_store()
    option_get=option_store()

    return pt.Seq(
     pt.Assert(app.state.proposal_question_chk==question_id.get()),

    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),


    (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.user_response),
    pt.Assert(user_response.get()==user_response_store.get()),

    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),

    (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),
    pt.Assert(question_id.get()==user_question_store.get()),
               
    question_store1.decode(app.state.question_rec[question_id.get()].get(),),
    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),

    user_store.decode(app.state.user_rec[user_id.get()].get()),

    (user_store1 :=pt.abi.make(pt.abi.String)).set(user_store.proposal_id),
    pt.Assert(user_store1.get()==proposal_id.get()),


    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
    (proposal_asset_count :=pt.abi.make(pt.abi.Uint64)).set(proposal_get.asset_count),
    (proposal_name :=pt.abi.make(pt.abi.String)).set(proposal_get.proposal_name),
    (proposal_Amount :=pt.abi.make(pt.abi.Uint64)).set(proposal_get.Amount),

    pt.Assert(token_buy.get()<=proposal_asset_count.get()),
    
    asset_store.decode(app.state.asset_rec[user_id.get()].get()),
    (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),
    app.state.user_amount_chk.set(user_token_store.get()+token_buy.get()),
    (amt_chk := pt.abi.Uint64()).set(app.state.user_amount_chk.get()),
                  
    (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_store.asset_id),
    (amt_chk1:= pt.abi.String()).set(user_asset_store.get()),

    asset_store.set(user_id,amt_chk1,amt_chk),
    app.state.asset_rec[user_id.get()].set(asset_store),
           
    (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.User_Token),
    (amt_chk2:= pt.abi.Uint64()).set(user_response_store.get()+token_buy.get()),
    (concat:=pt.abi.String()).set(pt.Concat(question_id.get(),user_id.get())),

    response_get.set(concat,amt_chk2,user_response,question_id),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].set(response_get),

    proposal_asset_count.set(proposal_asset_count.get()-token_buy.get()),
    proposal_get.set(proposal_id,proposal_name,proposal_asset_count,proposal_Amount),
    app.state.proposal_rec[proposal_id.get()].set(proposal_get),

#//options         
     option_get.decode(app.state.option_rec[question_id.get()].get()),
    (option_1_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_1),
    (option_2_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_2),     
    (option_3_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_3),
    (option_4_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_4),
    (option_5_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_5),
    (option_6_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_6),    
    (option_7_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_7),
  
    pt.If(user_response.get() == pt.Int(1)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_1_store.set(option_1_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(2)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_2_store.set(option_2_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(3)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_3_store.set(option_3_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(4)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_4_store.set(option_4_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(5)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_5_store.set(option_5_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(6)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_6_store.set(option_6_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

           ).ElseIf

    (user_response.get() == pt.Int(7)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_7_store.set(option_7_store.get() + token_buy.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

    ),
    )

#------------------------ Function to Sell Tokens in Secondary Market Place ------------------------

@app.external
def token_sell(proposal_id:pt.abi.String,user_id:pt.abi.String,question_id:pt.abi.String,
               user_response:pt.abi.Uint64,
               token_sell:pt.abi.Uint64)->pt.Expr:  
    
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    question_store1=Question_store()
    response_get = Response_store()
    asset_store = User_asset_store()
    option_get=option_store()

    return pt.Seq(
    pt.Assert(app.state.proposal_question_chk==question_id.get()),
    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),


    (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.user_response),
    pt.Assert(user_response.get()==user_response_store.get()),

    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),

    (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),
    pt.Assert(question_id.get()==user_question_store.get()),

    # response_get.decode(app.state.response_rec[user_id.get()].get()),
    response_get.decode(app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].get()),
    question_store1.decode(app.state.question_rec[question_id.get()].get()),
    user_store.decode(app.state.user_rec[user_id.get()].get()),


    (user_store1 :=pt.abi.make(pt.abi.String)).set(user_store.proposal_id),
    pt.Assert(user_store1.get()==proposal_id.get()),


    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),

    (proposal_asset_count :=pt.abi.make(pt.abi.Uint64)).set(proposal_get.asset_count),
    (proposal_name :=pt.abi.make(pt.abi.String)).set(proposal_get.proposal_name),
    (proposal_Amount :=pt.abi.make(pt.abi.Uint64)).set(proposal_get.Amount),

    asset_store.decode(app.state.asset_rec[user_id.get()].get()),
    (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),
    pt.Assert(token_sell.get()<=user_token_store.get()),
    app.state.user_amount_chk.set(user_token_store.get()-token_sell.get()),
    (amt_chk := pt.abi.Uint64()).set(app.state.user_amount_chk.get()),

    (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_store.asset_id),
    (amt_chk1:= pt.abi.String()).set(user_asset_store.get()),
    asset_store.set(user_id,amt_chk1,amt_chk),
    app.state.asset_rec[user_id.get()].set(asset_store),
 
    (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.User_Token),
    (amt_chk2:= pt.abi.Uint64()).set(user_response_store.get()-token_sell.get()),
    (concat:=pt.abi.String()).set(pt.Concat(question_id.get(),user_id.get())),

    response_get.set(concat,amt_chk2,user_response,question_id),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].set(response_get),   


    proposal_asset_count.set(proposal_asset_count.get()+token_sell.get()),
    proposal_get.set(proposal_id,proposal_name,proposal_asset_count,proposal_Amount),
    app.state.proposal_rec[proposal_id.get()].set(proposal_get),

# //options
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    (option_1_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_1),
    (option_2_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_2),
    (option_3_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_3),
    (option_4_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_4),
    (option_5_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_5),
    (option_6_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_6),
    (option_7_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_7),
 
 pt.If(user_response.get() == pt.Int(1)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_1_store.set(option_1_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(2)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_2_store.set(option_2_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(3)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_3_store.set(option_3_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf
 
    (user_response.get() == pt.Int(4)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_4_store.set(option_4_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf
                                                   
    (user_response.get() == pt.Int(5)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_5_store.set(option_5_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(6)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_6_store.set(option_6_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),

            ).ElseIf

    (user_response.get() == pt.Int(7)).Then(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    option_7_store.set(option_7_store.get() - token_sell.get()),
    option_get.set(question_id,option_1_store,option_2_store,option_3_store,option_4_store,option_5_store,option_6_store,option_7_store),
    app.state.option_rec[(question_id).get()].set(option_get),
    ),
    )                           

#------------------------------- Function to Calculate Result of the Voting --------------------------------

@app.external   
def Result(question_id:pt.abi.String,*,output:pt.abi.String)-> pt.Expr:
             
    question_store1=Question_store()
    option_get=option_store()

    return pt.Seq(
    question_store1.decode(app.state.question_rec[question_id.get()].get()), 

 # //Options
     option_get.decode(app.state.option_rec[question_id.get()].get()),
    (option_1_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_1),
    (option_2_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_2),
    (option_3_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_3),
    (option_4_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_4),
    (option_5_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_5),
    (option_6_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_6),
    (option_7_store:=pt.abi.make(pt.abi.Uint64)).set(option_get.option_7),
                           
    (maxi := pt.abi.Uint64()).set(option_1_store.get()),

    pt.If(option_2_store.get() > maxi.get()).Then(
                maxi.set(option_2_store.get())
                ),
    pt.If(option_3_store.get() > maxi.get()).Then(
                maxi.set(option_3_store.get())
                ),
    pt.If(option_4_store.get() > maxi.get()).Then(
                maxi.set(option_4_store.get())
                ),
    pt.If(option_5_store.get() > maxi.get()).Then(
                maxi.set(option_5_store.get())
                ),
    pt.If(option_6_store.get() > maxi.get()).Then(          
                maxi.set(option_6_store.get())
                ),
    pt.If(option_7_store.get() > maxi.get()).Then(
                maxi.set(option_7_store.get())
                ),

    pt.If(maxi.get() == option_1_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 1 is winner, "), question_id.get())),


    ).ElseIf(maxi.get() == option_2_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 2 is winner, "), question_id.get())),


    ).ElseIf(maxi.get() == option_3_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 3 is winner, "), question_id.get())),


    ).ElseIf(maxi.get() == option_4_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 4 is winner, "), question_id.get())),
  

    ).ElseIf(maxi.get() == option_5_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 5 is winner, "), question_id.get())),


    ).ElseIf(maxi.get() == option_6_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 6 is winner, "), question_id.get())),


    ).ElseIf(maxi.get() == option_7_store.get()).Then(
    output.set(pt.Concat(pt.Bytes("option 7 is winner, "), question_id.get())),

    ),
    )
       
#-------------------------------------- Read Functions ---------------------------------------

@app.external 
def read_options(question_id:pt.abi.String,*,output:option_store)-> pt.Expr:
    option_get=option_store()
    return pt.Seq(
    option_get.decode(app.state.option_rec[question_id.get()].get()),
    app.state.option_rec[question_id.get()].store_into(output)
    )

@app.external
def read_proposal_store(proposal_id:pt.abi.String,*,output:Proposal_Record2)-> pt.Expr:
    return app.state.proposal_rec2[proposal_id.get()].store_into(output)

@app.external
def read_current_proposal_store(proposal_id:pt.abi.String,*,output:Proposal_Record)-> pt.Expr:
    return app.state.proposal_rec[proposal_id.get()].store_into(output)

@app.external
def read_asset_id(asset_id:pt.abi.String,*,output:asset_store)-> pt.Expr:
    return app.state.asset_str[asset_id.get()].store_into(output)

@app.external
def read_user_proposal_store(proposal_id:pt.abi.String,user_id:pt.abi.String,*,output:User_per_proposal_record)-> pt.Expr:
    proposal_get = Proposal_Record()
    return pt.Seq(
    proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
    app.state.user_rec[user_id.get()].store_into(output)
    )

@app.external               
def read_user_asset_store(user_id:pt.abi.String,*,output:User_asset_store)-> pt.Expr:
    user_get = User_per_proposal_record()
    return pt.Seq(
    user_get.decode(app.state.user_rec[user_id.get()].get()),
    app.state.asset_rec[user_id.get()].store_into(output)
    )
  
@app.external
def read_user_response(user_id:pt.abi.String,question_id:pt.abi.String,*,output:Response_store)-> pt.Expr:
    user_get = User_per_proposal_record()
    return pt.Seq(
    user_get.decode(app.state.user_rec[user_id.get()].get()),
    app.state.response_rec[pt.Concat(question_id.get(),user_id.get())].store_into(output)

    )

# ----------------------------------------- App Build --------------------------------------------                  

if __name__=="__main__":
    spec=app.build()
    print("Contract Created Successfully!!!!!!!!!!")
    spec.export("artifacts_debug")

