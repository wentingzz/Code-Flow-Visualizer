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
        # ---------------------------------Simple if-------------------------
        # s = """
        # main
        # var a,b,c,d,e;
        # {
        #     let a<-call InputNum();
        #     let b<-a;
        #     let c<-b;
        #     let d<- b+ c;
        #     let e <-a+b;
        #     if a<0 then
        #         let d<-d+e;
        #         let a<- d
        #     else
        #         let d<- e
        #     fi;
        #     call OutputNum(a)
        # }."""


        # ---------------------------------If in While----------------------
        s = """main 
        var x,y,i,j; 
        {
            let i<-call InputNum(); 
            let x<-0; 
            let y<-0; 
            let j<- i; 
            while x<10 do  
                let x <- i + 1; 
                if x > 0 then 
                    let x <- j + 1 
                else 
                    let y <- i + 1 
                fi; 
                let i <-i + 1 
            od; 
            call OutputNum(x)
        }."""

        # -----------------------------------While in If-------------------
        # s = """
        # main
        # var x,y,i,j;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<- i;
        #     if j < 0 then
        #         let j <- x + 1;
        #         let x <- i + 1;
        #         while x<10 do
        #             let x <- j + 1 ;
        #             let y <- i + 1
        #         od;
        #     else
        #         let i <-i + 1
        #     fi;
        #     call OutputNum(x)
        # }."""
        # ------------------------------------2 Nested While-------------------------------
        # s = """
        # main
        # var x,y,i,j;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<- i;
        #     while x<10 do
        #         let x <- i + 1;
        #         let y <- j + 1;
        #         while j<10 do
        #             let x <- j + 1;
        #             let y <- i + 1;
        #             let j <-j + 1
        #         od;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x)
        # }."""
        # --------------------------------3 nested while loop------------------------
        # s = """
        # main
        # var x,y,i,j;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<- i;
        #     while x<10 do
        #         let x <- i + 1;
        #         let y <- j + 1;
        #         while j<10 do
        #             let x <- j + 1;
        #             while i < 10 do
        #                 let y <- i + 1
        #             od;
        #             let j <-j + 1
        #         od;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x)
        # }."""
        # ---------------------------Simple Array in If-----------------------
        # s = """
        # main
        # var a, b;
        # array[4] x;
        # {
        #     let a <- call InputNum ();
        #     let b <- a;
        #     let x[a] <- b + 2;
        #     if b<= 2 then
        #         let b <- x[a] + 2
        #     else
        #         let b <- x[b] + 2
        #     fi;
        #     call OutputNum(x[a])
        # }."""

        self.s = s