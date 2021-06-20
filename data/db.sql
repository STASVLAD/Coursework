-- Table: public.shopping_list

-- DROP TABLE public.shopping_list;

CREATE TABLE public.shopping_list
(
    id integer NOT NULL DEFAULT nextval('shopping_list_id_seq'::regclass),
    user_id character varying(64) COLLATE pg_catalog."default" NOT NULL,
    product character varying(64) COLLATE pg_catalog."default",
    quantity integer,
    created_on timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP,
    units character varying(64) COLLATE pg_catalog."default",
    frequency interval day[],
    CONSTRAINT shopping_list_pkey PRIMARY KEY (id),
    CONSTRAINT shopping_list_user_id_product_key UNIQUE (user_id, product)
)

TABLESPACE pg_default;

ALTER TABLE public.shopping_list
    OWNER to postgres;

-----------------------------------------------------------------------------

-- Table: public.product_prices

-- DROP TABLE public.product_prices;

CREATE TABLE public.product_prices
(
    product character varying(64) COLLATE pg_catalog."default" NOT NULL,
    price integer,
    CONSTRAINT product_prices_pkey PRIMARY KEY (product)
)

TABLESPACE pg_default;

ALTER TABLE public.product_prices
    OWNER to postgres;