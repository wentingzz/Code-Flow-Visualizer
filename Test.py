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

        # ----------------------------Array assignment in If----------------------
        # s = """
        # main
        # var a, b;
        # array[4] x;
        # {
        #     let a <- call InputNum ();
        #     let b <- a;
        #     let x[a] <- b + 2;
        #     if b<= 2 then
        #         let x[b] <- x[a] + 2
        #     else
        #         let b <- x[b] + 2
        #     fi;
        #     call OutputNum(x[a])
        # }."""
        # ------------------------Array in while with index changed----------------------
        # s = """
        # main
        # var x,y,i,j;
        # array[4] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<- i;
        #     let a[x] <- i;
        #     while x<10 do
        #         let x <- i + 1;
        #         let y <- a[x] + 1;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(a[x])
        # }."""
        # -------------------Array assignment in while with same index and same value------------------
        # s = """
        # main
        # var x,y,i,j;
        # array[4] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x] <- i;
        #     while i<10 do
        #         let j <- i + 1;
        #         let a[x] <- x + 1;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(a[x])
        # }."""
        # ------------------Array assignment in while with same index and different value
        # s = """
        # main
        # var x,y,i,j;
        # array[4] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x] <- i;
        #     while i<10 do
        #         let j <- i + 1;
        #         let a[x] <- a[x] + 1;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(a[x])
        # }."""

        # ------------------------Array in while with same index--------------------
        # s = """
        # main
        # var x,y,i,j;
        # array[4] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x] <- i;
        #     while i<10 do
        #         let j <- i + 1;
        #         let y <- a[x] + 1;
        #         let i <-i + 1
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(a[x])
        # }."""

        # --------------------Multidimensional Array in While-----------------------
        # s = """
        # main
        # var x,y,i,j;
        # array[4][3][2] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x][i] <- i;
        #     while i<10 do
        #         let j <- i + 1;
        #         let y <- a[x][i] + 1;
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(a[x][i])
        # }."""

        # s = """
        # main
        # var x,y,i,j;
        # array[4][3][2] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x][j] <- i;
        #     while j<10 do
        #         let j <- i + 1;
        #         let a[x][j] <- a[x][j] + 1;
        #         let y <-i + 1
        #     od;
        #     call OutputNum(y);
        #     call OutputNum(a[x][i])
        # }."""

        # --------------------Multidimensional Array in if-----------------------
        # s = """
        # main
        # var a, b;
        # array[4][3][2] x;
        # {
        #     let a <- call InputNum ();
        #     let b <- a;
        #     let i <- 0;
        #     let j <- i;
        #     let x[a][i][b] <- b + 2;
        #     if b<= 2 then
        #         let x[b][j][a] <- x[a][j][b] + 2
        #     else
        #         let b <- x[a][i][b] + 2
        #     fi;
        #     call OutputNum(x[a][i][b])
        # }."""

        # ----------------Array in nested if/while--------------
        # s = """
        # main
        # var x,y,i,j;
        # array[4][3][2] a;
        # {
        #     let i<-call InputNum();
        #     let x<-0;
        #     let y<-0;
        #     let j<-i;
        #     let a[x][j][i] <- i;
        #     while j<10 do
        #         let j <- i + 1;
        #         while y < 0 do
        #             let y <- a[x][j] + i;
        #             while i < 10 do
        #                 let i <- a[x][j] + i
        #             od;
        #         od;
        #         let y <- y + 1
        #     od;
        #     call OutputNum(x);
        #     call OutputNum(y);
        #     call OutputNum(j);
        #     call OutputNum(i);
        #     call OutputNum(a[x][j])
        # }."""
        self.s = s