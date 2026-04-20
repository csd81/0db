go
create or alter function dbo.fn_earlier_or_na
(
    @d1 datetime,
    @d2 datetime
)
returns varchar(20)
as
begin
    declare @res varchar(20)

    if @d1 is null or @d2 is null
        set @res = 'N.A.'
    else if @d1 <= @d2
        set @res = convert(varchar(20), @d1, 120)
    else
        set @res = convert(varchar(20), @d2, 120)

    return @res
end
go

select dbo.fn_earlier_or_na('2024-01-10', '2024-01-05') as eredmeny
select dbo.fn_earlier_or_na(null, '2024-01-05') as eredmeny
go
