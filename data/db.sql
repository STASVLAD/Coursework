-- Table: public.shopping_list

-- DROP TABLE public.shopping_list;

CREATE TABLE public.shopping_list
(
    id integer NOT NULL DEFAULT nextval('shopping_list_id_seq'::regclass),
    user_id character varying(64) COLLATE pg_catalog."default" NOT NULL,
    product character varying(40) COLLATE pg_catalog."default",
    quantity integer,
    created_on timestamp(0) without time zone NOT NULL,
    CONSTRAINT shopping_list_pkey PRIMARY KEY (id),
    CONSTRAINT shopping_list_user_id_product_key UNIQUE (user_id, product),
    CONSTRAINT quantity_check CHECK (quantity >= 0)
)

TABLESPACE pg_default;

ALTER TABLE public.shopping_list
    OWNER to postgres;