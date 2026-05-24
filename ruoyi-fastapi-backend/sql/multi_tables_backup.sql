--
-- PostgreSQL database dump
--

\restrict S4xDazMsdJ9RbecRrUtZcC4Ogf1RVE7yT6tBEmGpOrtSgIOGDaHckTaa7YCTGab

-- Dumped from database version 17.9 (Postgres.app)
-- Dumped by pg_dump version 17.9 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ChatSession; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."ChatSession" (
    id uuid NOT NULL,
    "userId" integer NOT NULL,
    title text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL
);


ALTER TABLE public."ChatSession" OWNER TO root;

--
-- Name: KnowledgeFile; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."KnowledgeFile" (
    id integer NOT NULL,
    filename text NOT NULL,
    filepath text NOT NULL,
    filetype text NOT NULL,
    filesize integer NOT NULL,
    md5 text NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "deletedAt" timestamp(3) without time zone
);


ALTER TABLE public."KnowledgeFile" OWNER TO root;

--
-- Name: KnowledgeFile_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public."KnowledgeFile_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."KnowledgeFile_id_seq" OWNER TO root;

--
-- Name: KnowledgeFile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public."KnowledgeFile_id_seq" OWNED BY public."KnowledgeFile".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    salt text NOT NULL
);


ALTER TABLE public."User" OWNER TO root;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_id_seq" OWNER TO root;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- Name: _prisma_migrations; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public._prisma_migrations OWNER TO root;

--
-- Name: agent_chat_messages; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.agent_chat_messages (
    id bigint NOT NULL,
    session_id uuid NOT NULL,
    payload jsonb NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "deletedAt" timestamp(3) without time zone,
    user_id integer NOT NULL
);


ALTER TABLE public.agent_chat_messages OWNER TO root;

--
-- Name: agent_chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.agent_chat_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agent_chat_messages_id_seq OWNER TO root;

--
-- Name: agent_chat_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.agent_chat_messages_id_seq OWNED BY public.agent_chat_messages.id;


--
-- Name: dishes; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.dishes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    image_url text[] NOT NULL,
    title text,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    content text NOT NULL,
    deleted_at timestamp(3) without time zone
);


ALTER TABLE public.dishes OWNER TO root;

--
-- Name: dishes_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.dishes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dishes_id_seq OWNER TO root;

--
-- Name: dishes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.dishes_id_seq OWNED BY public.dishes.id;


--
-- Name: KnowledgeFile id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."KnowledgeFile" ALTER COLUMN id SET DEFAULT nextval('public."KnowledgeFile_id_seq"'::regclass);


--
-- Name: User id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- Name: agent_chat_messages id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.agent_chat_messages ALTER COLUMN id SET DEFAULT nextval('public.agent_chat_messages_id_seq'::regclass);


--
-- Name: dishes id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.dishes ALTER COLUMN id SET DEFAULT nextval('public.dishes_id_seq'::regclass);


--
-- Data for Name: ChatSession; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public."ChatSession" (id, "userId", title, "createdAt", "updatedAt") FROM stdin;
810e2f1b-e462-4752-8500-78014b7d5bba	1	\N	2026-05-23 02:14:25.289	2026-05-23 02:14:25.289
\.


--
-- Data for Name: KnowledgeFile; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public."KnowledgeFile" (id, filename, filepath, filetype, filesize, md5, "createdAt", "updatedAt", "deletedAt") FROM stdin;
1	1777892406890-ebe17dfd-__.jpeg	http://private-chef-0424.oss-cn-beijing.aliyuncs.com/1779501015812-3c4ec4d6-1777892406890-ebe17dfd-__.jpeg?OSSAccessKeyId=LTAI5t8WFyEUDVrBsSrnusiz&Expires=1779587416&Signature=NrQTpkek%2BqgFElje%2ByV%2BhMkOCYE%3D	image/jpeg	90912	7b781fcbf988fe0c0632bf27b5b43373	2026-05-23 01:50:16.12	2026-05-23 01:50:16.12	\N
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public."User" (id, email, password, salt) FROM stdin;
1	413114463@qq.com	29d870b40c4fce66162db3a34bc1eaec18871e86ab2c23a82132ee816a28cf4e	cd8c5e944effa8492013f126c7e3f77e
2	aachen2012@outlook.com	d4f76246933e23516bf03156516727e62ef520633fb6d9b0dcafb87aafdfdb5e	39acc5a62c90ca0fc374b2f63854d08e
\.


--
-- Data for Name: _prisma_migrations; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public._prisma_migrations (id, checksum, finished_at, migration_name, logs, rolled_back_at, started_at, applied_steps_count) FROM stdin;
ddc4c63c-187a-4e13-bd21-631fcb96a933	0f64a28933f2e5112e25fb37228fcad4d9587c5d7d10d1581970b0e7b09cef9e	2026-05-23 09:48:38.92487+08	20260515022135_add_tbl_user	\N	\N	2026-05-23 09:48:38.921054+08	1
ab39909e-e392-4c23-a0dc-1c9d83d2a55e	65797d7ab89b1fc1f6fa85e59aa22b234b02cecd3cef58c71503d6aea5ee8963	2026-05-23 09:48:38.927857+08	20260517043049_add_tbl_knowledgefile	\N	\N	2026-05-23 09:48:38.925133+08	1
21249fca-be36-4d10-bbfd-ab3eb4e6b461	37e362f6dd287a7f4c8229d00969432aa3625026604185515f1dcc16eae9f347	2026-05-23 09:48:38.929102+08	20260518032335_add_col_salt	\N	\N	2026-05-23 09:48:38.928015+08	1
91b8845e-3b9c-4886-a2b8-1c4a6bdda380	551644f1837a54d9d6d7015d15dc571a2e570aae8415db76f09e747cd27fdfbb	2026-05-23 09:48:38.934221+08	20260520054647_add_tbl_chat	\N	\N	2026-05-23 09:48:38.929249+08	1
479bd5fb-0d61-4039-8d5e-91637d175814	f53888f2db6ce2bd984ab8c1aceedda65623cb846c2d9218fbcb6e44fcb59892	2026-05-23 09:48:38.939192+08	20260520120000_add_dish	\N	\N	2026-05-23 09:48:38.934418+08	1
56c75261-7b85-4c78-b2ff-4e075a476628	2f967930d38d29ef429e0e9a456773efeb6bb4587e1a340b84fee1d9b0c0290a	2026-05-23 09:48:38.941818+08	20260520140000_dish_image_url_array	\N	\N	2026-05-23 09:48:38.939397+08	1
e94ffebf-4415-4bca-8be1-15a4598e5d7b	d54a420e9c629ef0465c3596ab83e2ccc4a52f9bd87e140fbae1e37ce2975ff5	2026-05-23 09:48:38.943974+08	20260522120000_dish_content_soft_delete	\N	\N	2026-05-23 09:48:38.941991+08	1
\.


--
-- Data for Name: agent_chat_messages; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.agent_chat_messages (id, session_id, payload, "createdAt", "updatedAt", "deletedAt", user_id) FROM stdin;
1	810e2f1b-e462-4752-8500-78014b7d5bba	{"data": {"id": null, "name": null, "type": "human", "content": "123123", "additional_kwargs": {}, "response_metadata": {}}, "type": "human"}	2026-05-23 10:14:32.579	2026-05-23 10:14:32.579	\N	1
2	810e2f1b-e462-4752-8500-78014b7d5bba	{"data": {"id": null, "name": null, "type": "ai", "content": "您好！您输入的内容“123123”看起来像是测试信息或误输入。如果您有关于尺码选择的问题，比如想根据身高和体重查询合适的衣服尺码，请提供您的具体身高（厘米）和体重（斤），我会根据您提供的参考资料为您推荐对应的尺码建议。欢迎随时补充信息！", "tool_calls": [], "usage_metadata": null, "additional_kwargs": {}, "response_metadata": {}, "invalid_tool_calls": []}, "type": "ai"}	2026-05-23 10:14:32.579	2026-05-23 10:14:32.579	\N	1
\.


--
-- Data for Name: dishes; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.dishes (id, user_id, image_url, title, created_at, updated_at, content, deleted_at) FROM stdin;
1	1	{http://private-chef-0424.oss-cn-beijing.aliyuncs.com/1779501015812-3c4ec4d6-1777892406890-ebe17dfd-__.jpeg?OSSAccessKeyId=LTAI5t8WFyEUDVrBsSrnusiz&Expires=1779587416&Signature=NrQTpkek%2BqgFElje%2ByV%2BhMkOCYE%3D}	title	2026-05-23 01:50:21.24	2026-05-23 01:50:21.24	content	\N
\.


--
-- Name: KnowledgeFile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public."KnowledgeFile_id_seq"', 1, true);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public."User_id_seq"', 2, true);


--
-- Name: agent_chat_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.agent_chat_messages_id_seq', 2, true);


--
-- Name: dishes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.dishes_id_seq', 1, true);


--
-- Name: ChatSession ChatSession_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."ChatSession"
    ADD CONSTRAINT "ChatSession_pkey" PRIMARY KEY (id);


--
-- Name: KnowledgeFile KnowledgeFile_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."KnowledgeFile"
    ADD CONSTRAINT "KnowledgeFile_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: _prisma_migrations _prisma_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);


--
-- Name: agent_chat_messages agent_chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.agent_chat_messages
    ADD CONSTRAINT agent_chat_messages_pkey PRIMARY KEY (id);


--
-- Name: dishes dishes_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY (id);


--
-- Name: KnowledgeFile_filepath_key; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX "KnowledgeFile_filepath_key" ON public."KnowledgeFile" USING btree (filepath);


--
-- Name: KnowledgeFile_md5_key; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX "KnowledgeFile_md5_key" ON public."KnowledgeFile" USING btree (md5);


--
-- Name: User_email_key; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX "User_email_key" ON public."User" USING btree (email);


--
-- Name: agent_chat_messages_session_id_idx; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX agent_chat_messages_session_id_idx ON public.agent_chat_messages USING btree (session_id);


--
-- Name: agent_chat_messages_user_id_idx; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX agent_chat_messages_user_id_idx ON public.agent_chat_messages USING btree (user_id);


--
-- Name: dishes_user_id_idx; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX dishes_user_id_idx ON public.dishes USING btree (user_id);


--
-- Name: agent_chat_messages agent_chat_messages_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.agent_chat_messages
    ADD CONSTRAINT agent_chat_messages_session_id_fkey FOREIGN KEY (session_id) REFERENCES public."ChatSession"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: agent_chat_messages agent_chat_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.agent_chat_messages
    ADD CONSTRAINT agent_chat_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: dishes dishes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict S4xDazMsdJ9RbecRrUtZcC4Ogf1RVE7yT6tBEmGpOrtSgIOGDaHckTaa7YCTGab

