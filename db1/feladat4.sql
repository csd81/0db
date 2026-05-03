-- ÖNÁLLÓ FELADAT #4: az 1000-nél kisebb Fibonacci-számok kiíratása
SET NOCOUNT ON;                                                 
declare @a int = 1, @b int = 1, @c int;
declare @t table (n int, fib int);

insert @t values (1, @a), (2, @b);
declare @i int = 3;                                                                                                         

while 1 = 1                                                                                                                 
begin
    set @c = @a + @b;                                                                                                       
    if @c >= 1000 break;                                        
    insert @t values (@i, @c);                                                                                              
    set @a = @b; set @b = @c; set @i += 1;
end                                                                                                                         

select n, fib from @t order by n;  		