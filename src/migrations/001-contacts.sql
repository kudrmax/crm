create table if not exists contacts
(
    id         serial primary key,
    name       varchar(255) not null unique,
    phone      varchar(20),
    telegram   varchar(50),
    birthday   varchar(10)
);