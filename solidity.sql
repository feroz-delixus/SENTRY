--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-1.pgdg18.04+1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: contracts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contracts (
    contractid integer NOT NULL,
    scanid integer,
    contractname character varying(250),
    datepresent timestamp with time zone DEFAULT now()
);


ALTER TABLE public.contracts OWNER TO postgres;

--
-- Name: contracts_contractid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contracts_contractid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contracts_contractid_seq OWNER TO postgres;

--
-- Name: contracts_contractid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contracts_contractid_seq OWNED BY public.contracts.contractid;


--
-- Name: files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files (
    fileid integer NOT NULL,
    scanid integer,
    filename character varying(250),
    datepresent timestamp with time zone DEFAULT now()
);


ALTER TABLE public.files OWNER TO postgres;

--
-- Name: files_fileid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.files_fileid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.files_fileid_seq OWNER TO postgres;

--
-- Name: files_fileid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.files_fileid_seq OWNED BY public.files.fileid;


--
-- Name: issues; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issues (
    issueid integer NOT NULL,
    scanid integer,
    contractid integer,
    swcid character varying(20),
    descriptionhead character varying(1000),
    descriptiontail character varying(1000),
    swctitle character varying(200),
    linenum integer,
    filename character(100),
    datepresent timestamp with time zone DEFAULT now(),
    severity character varying(50)
);


ALTER TABLE public.issues OWNER TO postgres;

--
-- Name: issues_issueid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issues_issueid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issues_issueid_seq OWNER TO postgres;

--
-- Name: issues_issueid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issues_issueid_seq OWNED BY public.issues.issueid;


--
-- Name: solidityscans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solidityscans (
    scanid integer NOT NULL,
    scanname character varying(250) NOT NULL,
    path character varying(250) NOT NULL,
    result text,
    datepresent timestamp with time zone DEFAULT now()
);


ALTER TABLE public.solidityscans OWNER TO postgres;

--
-- Name: solidityscans_scanid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.solidityscans_scanid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.solidityscans_scanid_seq OWNER TO postgres;

--
-- Name: solidityscans_scanid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.solidityscans_scanid_seq OWNED BY public.solidityscans.scanid;


--
-- Name: contracts contractid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts ALTER COLUMN contractid SET DEFAULT nextval('public.contracts_contractid_seq'::regclass);


--
-- Name: files fileid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files ALTER COLUMN fileid SET DEFAULT nextval('public.files_fileid_seq'::regclass);


--
-- Name: issues issueid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues ALTER COLUMN issueid SET DEFAULT nextval('public.issues_issueid_seq'::regclass);


--
-- Name: solidityscans scanid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solidityscans ALTER COLUMN scanid SET DEFAULT nextval('public.solidityscans_scanid_seq'::regclass);


--
-- Name: contracts contracts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (contractid);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (fileid);


--
-- Name: issues issues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issues_pkey PRIMARY KEY (issueid);


--
-- Name: solidityscans solidityscans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solidityscans
    ADD CONSTRAINT solidityscans_pkey PRIMARY KEY (scanid);


--
-- Name: contracts contracts_scanid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_scanid_fkey FOREIGN KEY (scanid) REFERENCES public.solidityscans(scanid) ON DELETE CASCADE;


--
-- Name: files files_scanid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_scanid_fkey FOREIGN KEY (scanid) REFERENCES public.solidityscans(scanid) ON DELETE CASCADE;


--
-- Name: issues issues_contractid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issues_contractid_fkey FOREIGN KEY (contractid) REFERENCES public.contracts(contractid) ON DELETE CASCADE;


--
-- Name: issues issues_scanid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issues_scanid_fkey FOREIGN KEY (scanid) REFERENCES public.solidityscans(scanid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
