-- ÖNÁLLÓ FELADAT #4: az 1000-nél kisebb Fibonacci-számok kiíratása
declare @a int = 1,
        @b int = 1,
        @c int

print @a
print @b

while 1 = 1
begin
    set @c = @a + @b

    if @c >= 1000
        break

    print @c

    set @a = @b
    set @b = @c
end
go
