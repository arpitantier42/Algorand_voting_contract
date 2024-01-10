import beaker as bk
import pyteal as pt
from beaker.lib.storage import BoxMapping



class Proposal_Record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]=""
    proposal_name:pt.abi.Field[pt.abi.String]=[]
    asset_count:pt.abi.Field[pt.abi.Uint64]=[]
    Amount:pt.abi.Field[pt.abi.Uint64]=[]
    
class asset_store(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    asset_id:pt.abi.Field[pt.abi.String]=[]

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

class Result_store(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    question_id:pt.abi.Field[pt.abi.String]
    result:pt.abi.Field[pt.abi.Uint64]

class Proposal_Record_State:
    proposal_rec = BoxMapping(pt.abi.String,Proposal_Record)
    user_rec = BoxMapping(pt.abi.String,User_per_proposal_record,prefix=pt.Bytes("_"))
    asset_rec = BoxMapping(pt.abi.String,User_asset_store,prefix=pt.Bytes("#"))
    response_rec = BoxMapping(pt.abi.String,Response_store,prefix=pt.Bytes("@"))
    asset_str = BoxMapping(pt.abi.String,asset_store,prefix=pt.Bytes("$"))
    question_rec = BoxMapping(pt.abi.String,Question_store,prefix=pt.Bytes("Q"))
    result_rec= BoxMapping(pt.abi.String,Result_store,prefix=pt.Bytes("R"))

# Some Global Variable declaration
    result_proposal_id =bk.GlobalStateValue(
        pt.TealType.uint64
    )

    option1 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option2 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option3 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option4 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option5 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),  
    )
    option6 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option7 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option8 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option9 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    option10 = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    response = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    asset_amount_str = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    asset_amount_chk = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    user_amount_chk = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
 
app =(
     bk.Application("Voting_Contract_fn_test",state = Proposal_Record_State())
     .apply(bk.unconditional_create_approval,initialize_global_state=True)
)

# Function to Register Proposal
@app.external
def Register_proposal(proposal_id:pt.abi.String, proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,Amount:pt.abi.Uint64,* ,output:Proposal_Record) -> pt.Expr:

    proposal_store = Proposal_Record()
   
    return pt.Seq(
    app.state.option1.set(pt.Int(0)),
    app.state.option2.set(pt.Int(0)),
    app.state.option3.set(pt.Int(0)),
    app.state.option4.set(pt.Int(0)),
    app.state.option5.set(pt.Int(0)),
    app.state.option6.set(pt.Int(0)),
    app.state.option7.set(pt.Int(0)),
    app.state.option8.set(pt.Int(0)),
    app.state.option9.set(pt.Int(0)),
    app.state.option10.set(pt.Int(0)),
    app.state.response.set(pt.Int(0)),
    app.state.asset_amount_str.set(pt.Int(0)),
    app.state.asset_amount_chk.set(pt.Int(0)),
    app.state.user_amount_chk.set(pt.Int(0)),

        app.state.asset_amount_str.set(asset_count.get()),
        app.state.asset_amount_chk.set(asset_count.get()),

        proposal_store.set(proposal_id,proposal_name,asset_count,Amount),
        pt.Assert(app.state.proposal_rec[proposal_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"
        ),
        pt.Log(pt.Bytes("proposal already registered")),

        app.state.proposal_rec[proposal_id.get()].set(proposal_store),
        app.state.proposal_rec[proposal_id.get()].store_into(output),
     )

#Function to Register Multiple Questions
@app.external
def RegisterQues(proposal_id:pt.abi.String,question_id:pt.abi.String,question:pt.abi.String,* ,output:Question_store)->pt.Expr:

    proposal_get = Proposal_Record()
    question_store1=Question_store()
    
    return pt.Seq(
    app.state.option1.set(pt.Int(0)),
    app.state.option2.set(pt.Int(0)),
    app.state.option3.set(pt.Int(0)),
    app.state.option4.set(pt.Int(0)),
    app.state.option5.set(pt.Int(0)),
    app.state.option6.set(pt.Int(0)),
    app.state.option7.set(pt.Int(0)),
    app.state.option8.set(pt.Int(0)),
    app.state.option9.set(pt.Int(0)),
    app.state.option10.set(pt.Int(0)),

        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        question_store1.set(proposal_id,question_id,question),
        pt.Assert(app.state.question_rec[question_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),

        app.state.question_rec[question_id.get()].set(question_store1),
        app.state.question_rec[question_id.get()].store_into(output),
      )

#Function to Register user per proposal
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
#Function to Register Assets in the proposal
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

#Function to Register user per asset
@app.external
def Register_user_asset(proposal_id:pt.abi.String,user_id:pt.abi.String,
     asset_id:pt.abi.String,token_count:pt.abi.Uint64,*,output:pt.abi.String)-> pt.Expr:
    
    asset_register = User_asset_store()
    registred_user = User_per_proposal_record()
    existing_proposal_store = Proposal_Record()
    asset_get = asset_store()

    return pt.Seq(
        # (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_store.asset_id),


        pt.Assert(app.state.asset_amount_str.get()>=token_count.get()),
        existing_proposal_store.decode(app.state.proposal_rec[proposal_id.get()].get()),
        registred_user.decode(app.state.user_rec[user_id.get()].get()),
        asset_get.decode(app.state.asset_str[asset_id.get()].get()),

        pt.If(app.state.asset_rec[user_id.get()].exists()== pt.Int(0)).Then(
                asset_register.set(user_id,asset_id,token_count),
                app.state.asset_rec[(user_id).get()].set(asset_register),
                app.state.asset_amount_str.decrement(token_count.get()),
                app.state.asset_rec[user_id.get()].store_into(output),

        ).Else(
                asset_register.decode(app.state.asset_rec[user_id.get()].get()),

                    (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_register.asset_id),
                    pt.Assert(asset_id.get()!=user_asset_store.get()),

                    (token_count_update :=pt.abi.make(pt.abi.Uint64)).set(asset_register.User_Token),
                    token_count_update.set(token_count_update.get()+token_count.get()),

                    asset_register.set(user_id,asset_id,token_count_update),
                    app.state.asset_rec[(user_id).get()].set(asset_register),
                    app.state.asset_amount_str.decrement(token_count.get()),
                    app.state.asset_rec[user_id.get()].store_into(output), 
                )
)

#Function for Voting per proposal
@app.external
def Voting_Record(proposal_id:pt.abi.String,user_id:pt.abi.String,
                  token_count:pt.abi.Uint64,question_id:pt.abi.String,
                  user_response:pt.abi.Uint64,*,output:Response_store)-> pt.Expr:
     
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    asset_store = User_asset_store()
    response_get = Response_store()
    
    return pt.Seq(
     
   pt.Assert(user_response.get()<=pt.Int(10)),
   pt.Assert(user_response.get()>=pt.Int(1)),

        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        user_store.decode(app.state.user_rec[user_id.get()].get()),
        asset_store.decode(app.state.asset_rec[user_id.get()].get()),

        
        pt.If(app.state.response_rec[user_id.get()].exists()== pt.Int(0)).Then(

        response_get.set(user_id,token_count,user_response,question_id),
        app.state.response_rec[user_id.get()].set(response_get),
        app.state.response_rec[user_id.get()].store_into(output),

        ).Else(
                response_get.decode(app.state.response_rec[user_id.get()].get()),

            (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),
         pt.Assert(question_id.get()!=user_question_store.get()),

           response_get.set(user_id,token_count,user_response,question_id),
        app.state.response_rec[user_id.get()].set(response_get),
        app.state.response_rec[user_id.get()].store_into(output), 
        ),

        asset_store.decode(app.state.asset_rec[user_id.get()].get()),
        (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),

        pt.Assert(user_token_store.get()==token_count.get()),
        
        pt.If (user_response.get() == pt.Int(1)).Then(
        app.state.option1.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(2)).Then(
        app.state.option2.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(3)).Then(
            app.state.option3.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(4)).Then(
            app.state.option4.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(5)).Then(
                app.state.option5.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(6)).Then(
                app.state.option6.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(7)).Then(
                app.state.option7.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(8)).Then(
                app.state.option8.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(9)).Then(
                app.state.option9.increment(token_count.get())
        ).ElseIf(
            user_response.get() == pt.Int(10)).Then(
                app.state.option10.increment(token_count.get())
            ) ,  
    )

#Function to buy tokens in secondary market place
@app.external
def token_buy(proposal_id:pt.abi.String,
              user_id:pt.abi.String,question_id:pt.abi.String,user_response:pt.abi.Uint64,
              token_buy:pt.abi.Uint64)->pt.Expr:
    
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    question_store1=Question_store()
    response_get = Response_store()
    asset_store = User_asset_store()

    return pt.Seq(

# """""""
            response_get.decode(app.state.response_rec[user_id.get()].get()),
            (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.user_response),
            pt.Assert(user_response.get()==user_response_store.get()),


            response_get.decode(app.state.response_rec[user_id.get()].get()),

            (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),

            pt.Assert(question_id.get()==user_question_store.get()),

# """""""
            question_store1.decode(app.state.question_rec[question_id.get()].get(),),
            response_get.decode(app.state.response_rec[user_id.get()].get()),
            user_store.decode(app.state.user_rec[user_id.get()].get()),
            proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),

            pt.Assert(token_buy.get()<=app.state.asset_amount_str.get()),

            asset_store.decode(app.state.asset_rec[user_id.get()].get()),

            (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),
            app.state.user_amount_chk.set(user_token_store.get()+token_buy.get()),
            (amt_chk := pt.abi.Uint64()).set(app.state.user_amount_chk.get()),


            (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_store.asset_id),
            (amt_chk1:= pt.abi.String()).set(user_asset_store.get()),

            asset_store.set(user_id,amt_chk1,amt_chk),
            app.state.asset_rec[user_id.get()].set(asset_store),
# ////

            (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.User_Token),
            (amt_chk2:= pt.abi.Uint64()).set(user_response_store.get()+token_buy.get()),
            response_get.set(user_id,amt_chk2,user_response,question_id),
            app.state.response_rec[user_id.get()].set(response_get),

# ////
            app.state.asset_amount_str.decrement(token_buy.get()),


            pt.If (user_response.get() == pt.Int(1)).Then(
                    app.state.option1.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(2)).Then(
                    app.state.option2.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(3)).Then(
                    app.state.option3.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(4)).Then(
                    app.state.option4.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(5)).Then(
                    app.state.option5.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(6)).Then(
                    app.state.option6.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(7)).Then(
                    app.state.option7.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(8)).Then(
                    app.state.option8.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(9)).Then(
                    app.state.option9.increment(token_buy.get())
                    ).ElseIf
            (user_response.get() == pt.Int(10)).Then(
                    app.state.option10.increment(token_buy.get())
                    ),
    )

#Function to sell tokens in secondary market place
@app.external
def token_sell(proposal_id:pt.abi.String,user_id:pt.abi.String,question_id:pt.abi.String,
               user_response:pt.abi.Uint64,
               token_sell:pt.abi.Uint64)->pt.Expr:  
             
      proposal_get = Proposal_Record()
      user_store = User_per_proposal_record()
      question_store1=Question_store()
      response_get = Response_store()
      asset_store = User_asset_store()
                                                       
      return pt.Seq(
        response_get.decode(app.state.response_rec[user_id.get()].get()),
        (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.user_response),
        pt.Assert(user_response.get()==user_response_store.get()),


        response_get.decode(app.state.response_rec[user_id.get()].get()),
        (user_question_store :=pt.abi.make(pt.abi.String)).set(response_get.question),
        pt.Assert(question_id.get()==user_question_store.get()),

        
        response_get.decode(app.state.response_rec[user_id.get()].get()),
        question_store1.decode(app.state.question_rec[question_id.get()].get()),
        user_store.decode(app.state.user_rec[user_id.get()].get()),
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),

        
        asset_store.decode(app.state.asset_rec[user_id.get()].get()),
        (user_token_store :=pt.abi.make(pt.abi.Uint64)).set(asset_store.User_Token),
        pt.Assert(token_sell.get()<=user_token_store.get()),
        app.state.user_amount_chk.set(user_token_store.get()-token_sell.get()),
        (amt_chk := pt.abi.Uint64()).set(app.state.user_amount_chk.get()),
        
       
        (user_asset_store :=pt.abi.make(pt.abi.String)).set(asset_store.asset_id),
        (amt_chk1:= pt.abi.String()).set(user_asset_store.get()),
        asset_store.set(user_id,amt_chk1,amt_chk),
        app.state.asset_rec[user_id.get()].set(asset_store),

# ////
        (user_response_store :=pt.abi.make(pt.abi.Uint64)).set(response_get.User_Token),
            (amt_chk2:= pt.abi.Uint64()).set(user_response_store.get()-token_sell.get()),
        response_get.set(user_id,amt_chk2,user_response,question_id),
            app.state.response_rec[user_id.get()].set(response_get),
# ////
        app.state.asset_amount_str.increment(token_sell.get()),
        pt.If (user_response.get() == pt.Int(1)).Then(
                app.state.option1.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(2)).Then(
                app.state.option2.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(3)).Then(
                app.state.option3.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(4)).Then(
                app.state.option4.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(5)).Then(
                app.state.option5.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(6)).Then(
                app.state.option6.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(7)).Then(
                app.state.option7.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(8)).Then(
                app.state.option8.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(9)).Then(
                app.state.option9.decrement(token_sell.get())
                ).ElseIf
        (user_response.get() == pt.Int(10)).Then(
                app.state.option10.decrement(token_sell.get())
                ),
    )
     
#Function to Calculate Result of the voting
@app.external   
def Result(proposal_id:pt.abi.String,
           question_id:pt.abi.String,*,output:pt.abi.String)-> pt.Expr:
             
    proposal_get = Proposal_Record()
    app.state.result_proposal_id=app.state.result_proposal_id+pt.Int(1)
    question_store1=Question_store()
    result_store1=Result_store()
    return pt.Seq(
        
        question_store1.decode(app.state.question_rec[question_id.get()].get()),
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        (maxi := pt.abi.Uint64()).set(app.state.option1.get()),
         pt.If (app.state.option2.get() > maxi.get()).Then(
                        maxi.set(app.state.option2.get())
                        ),
            pt.If(app.state.option3.get() > maxi.get()).Then(
                        maxi.set(app.state.option3.get())
                        ),
            pt.If(app.state.option4.get()> maxi.get()).Then(
                        maxi.set(app.state.option4.get())
                        ),
            pt.If(app.state.option5.get()>maxi.get()).Then(
                        maxi.set(app.state.option5.get())
                        ),
            pt.If(app.state.option6.get()>maxi.get()).Then(          
                        maxi.set(app.state.option6.get())
                        ),
            pt.If(app.state.option7.get()>maxi.get()).Then(
                        maxi.set(app.state.option7.get())
                        ),
            pt.If(app.state.option8.get()>maxi.get()).Then(
                        maxi.set(app.state.option8.get())
                        ),
            pt.If(app.state.option9.get()>maxi.get()).Then(
                        maxi.set(app.state.option9.get())
                        ),
            pt.If(app.state.option10.get()>maxi.get()).Then(
                        maxi.set(app.state.option10.get()),      
                        ),

            pt.If(maxi.get() == app.state.option1.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 1 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(1)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option2.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 2 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(2)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option3.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 3 is winner, "), question_id.get())),
            (result:= pt.abi.Uint64()).set(pt.Int(3)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option4.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 4 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(4)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()==app.state.option5.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 5 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(5)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option6.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 6 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(6)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option7.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 7 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(7)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option8.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 8 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(8)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),

            ).ElseIf(maxi.get()== app.state.option9.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 9 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(9)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),
            ).ElseIf(maxi.get()== app.state.option10.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 10 is winner, "), question_id.get())),

            (result:= pt.abi.Uint64()).set(pt.Int(10)),
            result_store1.set(proposal_id,question_id,result),
            app.state.result_rec[question_id.get()].set(result_store1),
            ),
    )

#function to show the result wrt question_id
@app.external
def read_result(proposal_id:pt.abi.String,question_id:pt.abi.String,*,output:Result_store)->pt.Expr:
    proposal_get = Proposal_Record()
    question_store1=Question_store()

    return pt.Seq(
     question_store1.decode(app.state.question_rec[question_id.get()].get()),
     proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
     app.state.result_rec[question_id.get()].store_into(output)

    )

# Read Functions for the Proposal
@app.external
def option_1(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option1.get()))

@app.external
def read_remaining(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.asset_amount_str.get()))

@app.external
def option_2(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option2.get()))
    
@app.external
def option_3(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option3.get()))

@app.external
def option_4(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option4.get()))

@app.external
def option_5(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option5.get()))

@app.external
def option_6(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option6.get()))

@app.external
def option_7(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option7.get()))

@app.external
def option_8(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option8.get()))

@app.external
def option_9(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option9.get()))

@app.external
def option_10(*,output:pt.abi.Uint64)-> pt.Expr:
    return (output.set(app.state.option10.get()))

@app.external
def read_proposal_store(proposal_id:pt.abi.String,*,output:Proposal_Record)-> pt.Expr:
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
def read_user_asset_store(proposal_id:pt.abi.String,user_id:pt.abi.String,asset_id:pt.abi.String,*,output:User_asset_store)-> pt.Expr:
    proposal_get = Proposal_Record()
    user_get = User_per_proposal_record()
    return pt.Seq(
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        user_get.decode(app.state.user_rec[user_id.get()].get()),
        app.state.asset_rec[user_id.get()].store_into(output)
        )

@app.external
def read_user_response(user_id:pt.abi.String,question_id:pt.abi.String,proposal_id:pt.abi.String,*,output:Response_store)-> pt.Expr:
    proposal_get = Proposal_Record()
    user_get = User_per_proposal_record()
    return pt.Seq(
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        user_get.decode(app.state.user_rec[user_id.get()].get()),
        app.state.response_rec[user_id.get()].store_into(output))


if __name__=="__main__":
    spec=app.build()
    print("Contract Created Successfully!!!!!!!!!!")
    spec.export("artifacts_debug")
    
