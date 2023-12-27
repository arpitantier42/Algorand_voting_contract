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
    asset_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]
    user_response:pt.abi.Field[pt.abi.Uint64]
    question:pt.abi.Field[pt.abi.String]
  
class Question_store(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    question_id:pt.abi.Field[pt.abi.String]
    question_name:pt.abi.Field[pt.abi.String]

class Proposal_Record_State:
    proposal_rec = BoxMapping(pt.abi.String,Proposal_Record)
    user_rec = BoxMapping(pt.abi.String,User_per_proposal_record,prefix=pt.Bytes("_"))
    asset_rec = BoxMapping(pt.abi.String,User_asset_store,prefix=pt.Bytes("#"))
    response_rec = BoxMapping(pt.abi.String,Response_store,prefix=pt.Bytes("@"))
    asset_str = BoxMapping(pt.abi.String,asset_store,prefix=pt.Bytes("$"))
    question_rec = BoxMapping(pt.abi.String,Question_store,prefix=pt.Bytes("Q"))
 
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
    res = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )
    token_chk = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
    )

app =(
     bk.Application("Voting_Contract_fn_test",state = Proposal_Record_State())
     .apply(bk.unconditional_create_approval,initialize_global_state=True)
)

@app.external
def Register_proposal(proposal_id:pt.abi.String, proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,Amount:pt.abi.Uint64,* ,output:Proposal_Record) -> pt.Expr:

    proposal_store = Proposal_Record()

    return pt.Seq(
        proposal_store.set(proposal_id,proposal_name,asset_count,Amount),
        pt.Assert(app.state.proposal_rec[proposal_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"
        ),
        app.state.proposal_rec[proposal_id.get()].set(proposal_store),
       app.state.proposal_rec[proposal_id.get()].store_into(output),
    )

@app.external
def RegisterQues(proposal_id:pt.abi.String,question_id:pt.abi.String,question:pt.abi.String,* ,output:Question_store)->pt.Expr:

    proposal_get = Proposal_Record()
    question_store1=Question_store()
      
    return pt.Seq(
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        question_store1.set(proposal_id,question_id,question),
        app.state.question_rec[question_id.get()].set(question_store1),
        app.state.question_rec[question_id.get()].store_into(output),
      )

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

@app.external
def Register_user_asset(proposal_id:pt.abi.String,user_id:pt.abi.String,
     asset_id:pt.abi.String,token_count:pt.abi.Uint64,*,output:User_asset_store)-> pt.Expr:
    
    asset_register = User_asset_store()
    registred_user = User_per_proposal_record()
    existing_proposal_store = Proposal_Record()
    asset_get = asset_store()

    return pt.Seq(
        existing_proposal_store.decode(app.state.proposal_rec[proposal_id.get()].get()),
        registred_user.decode(app.state.user_rec[user_id.get()].get()),
        asset_get.decode(app.state.asset_str[asset_id.get()].get()),
        app.state.token_chk.set(token_count.get()),
        asset_register.set(user_id,asset_id,token_count),
        app.state.asset_rec[(asset_id).get()].set(asset_register),
        app.state.asset_rec[asset_id.get()].store_into(output),
    )

@app.external
def Voting_Record(proposal_id:pt.abi.String,user_id:pt.abi.String,asset_id:pt.abi.String,
                  token_count:pt.abi.Uint64,question_id:pt.abi.String,
                  user_response:pt.abi.Uint64,*,output:Response_store)-> pt.Expr:
    
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    asset_store = User_asset_store()
    response_get = Response_store()

    return pt.Seq(
        # Validating user_id and proposal_id to ensure data integrity.
        # question_store1.decode(app.state.question_rec[question_id.get()].get()),
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        user_store.decode(app.state.user_rec[user_id.get()].get()),
        asset_store.decode(app.state.asset_rec[asset_id.get()].get()),
        pt.Assert(app.state.response_rec[asset_id.get()].exists()==pt.Int(0),comment="User_ID already exists"),
        # here we have created a additional functionality user can input the token_count for the voting weightage.
        # He can input the amout on token count he want to use for voting.
        response_get.set(user_id,asset_id,token_count,user_response,question_id),
        app.state.response_rec[asset_id.get()].set(response_get),
        app.state.response_rec[asset_id.get()].store_into(output),
        pt.Assert(token_count.get()<=app.state.token_chk,comment="insufficient token_count"),
                  
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
                )                
    )

@app.external
def token_buy(proposal_id:pt.abi.String,
              user_id:pt.abi.String,asset_id:pt.abi.String,question_id:pt.abi.String,user_response:pt.abi.Uint64,
              token_buy:pt.abi.Uint64)->pt.Expr:
    
    proposal_get = Proposal_Record()
    user_store = User_per_proposal_record()
    question_store1=Question_store()
    response_get = Response_store()

    return pt.Seq(
                question_store1.decode(app.state.question_rec[question_id.get()].get()),
                response_get.decode(app.state.response_rec[asset_id.get()].get()),
                user_store.decode(app.state.user_rec[user_id.get()].get()),
                proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),

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
            )
    )

@app.external
def token_sell(proposal_id:pt.abi.String,user_id:pt.abi.String,asset_id:pt.abi.String,question_id:pt.abi.String,
               user_response:pt.abi.Uint64,
               token_sell:pt.abi.Uint64)->pt.Expr:  
             
      proposal_get = Proposal_Record()
      user_store = User_per_proposal_record()
      question_store1=Question_store()
      response_get = Response_store()

      return pt.Seq(
            response_get.decode(app.state.response_rec[asset_id.get()].get()),
            question_store1.decode(app.state.question_rec[question_id.get()].get()),
            user_store.decode(app.state.user_rec[user_id.get()].get()),
            proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
     
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
            )
    )

@app.external   
def Result(proposal_id:pt.abi.String,
           question_id:pt.abi.String,*,output:pt.abi.String)-> pt.Expr:
    
    proposal_get = Proposal_Record()
    app.state.result_proposal_id=app.state.result_proposal_id+pt.Int(1)
    question_store1=Question_store()

    return pt.Seq(
        question_store1.decode(app.state.question_rec[question_id.get()].get()),
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        (maxi := pt.abi.Uint64()).set(app.state.option1.get()),
         pt.If (app.state.option2.get() > maxi.get()).Then(
            maxi.set(app.state.option2.get())
            ).ElseIf(
                (app.state.option3.get() > maxi.get())).Then(
                maxi.set(app.state.option3.get())
                ).ElseIf(
                    app.state.option4.get()> maxi.get()).Then(
                        maxi.set(app.state.option4.get())
                    ).ElseIf(
                        app.state.option5.get()>maxi.get()).Then(
                            maxi.set(app.state.option5.get())
                        ).ElseIf(
                            app.state.option6.get()>maxi.get()).Then(
                            maxi.set(app.state.option6.get())
                        ).ElseIf(                       
                            app.state.option7.get()>maxi.get()).Then(
                         maxi.set(app.state.option7.get())
                        ).ElseIf(app.state.option8.get()>maxi.get()).Then(
                            maxi.set(app.state.option8.get())
                        ).ElseIf(app.state.option9.get()>maxi.get()).Then(
                            maxi.set(app.state.option9.get())
                        ).ElseIf(app.state.option10.get()>maxi.get()).Then(
                            maxi.set(app.state.option10.get()),      
                        ),
                            
        pt.If(maxi.get() == app.state.option1.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 1 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option2.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 2 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option3.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 3 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option4.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 4 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()==app.state.option5.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 5 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option6.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 6 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option7.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 7 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option8.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 8 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option9.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 9 is winner, "), question_id.get()))
        ).ElseIf(maxi.get()== app.state.option10.get()).Then(
            output.set(pt.Concat(pt.Bytes("option 10 is winner, "), question_id.get()))
        ),
    )

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
        app.state.asset_rec[asset_id.get()].store_into(output)
        )
    
@app.external
def read_user_response(user_id:pt.abi.String,asset_id:pt.abi.String,proposal_id:pt.abi.String,*,output:Response_store)-> pt.Expr:
    proposal_get = Proposal_Record()
    user_get = User_per_proposal_record()
    return pt.Seq(
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        user_get.decode(app.state.user_rec[user_id.get()].get()),
        app.state.response_rec[asset_id.get()].store_into(output))

if __name__=="__main__":
    spec=app.build()
    print("Contract Created Successfully!!!!!!!!!!")
    spec.export("artifacts_debug")

