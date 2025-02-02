create table if not exists logs
(
    id         serial primary key,
    contact_id int,
    text       varchar(1000) not null,
    datetime   timestamptz   not null default now(),

    foreign key (contact_id) references contacts (id) on delete cascade
);