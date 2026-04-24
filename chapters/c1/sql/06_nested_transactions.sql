USE northwind;
GO

begin tran
        print @@trancount  --1
        begin tran
                print @@trancount  --2
        commit tran
        print @@trancount  --1
commit tran
print @@trancount  --0

begin tran
        print @@trancount  --1
        begin tran
                print @@trancount  --2
rollback tran
print @@trancount  --0
