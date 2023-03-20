class Test:
    def getS(self):
        return self.s
    def __init__(self):
        self.past()

    def past(self):
        # -----------------------------------Nested if-------------------------------
        s = """
        main
        var a, b, c, d, e;  
        {
            let a <- call InputNum ( ); 
            let b<- a ;
            let c   <- b; 
            let d<-b+c; 
            let e<- a+b;  
            if a < 0 then 
                let d <- d+e;   
                if d != 0 then 
                    let a <- d 
                fi; 
            else   
                let d<-a; 
                if e >= 1 then 
                    let e <- a 
                else 
                    let e<-1 
                fi; 
                let a <- c 
            fi; 
            call OutputNum  ( a ) 
        }."""

        self.s = s