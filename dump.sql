--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

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
-- Name: complaint; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaint (
    complaint_id integer NOT NULL,
    category character varying(100),
    complaint_text text,
    summary text,
    urgency integer,
    title character varying(10),
    first_name character varying(100),
    last_name character varying(100),
    email character varying(100),
    telephone character varying(20),
    address character varying(255),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    longitude double precision,
    latitude double precision
);


ALTER TABLE public.complaint OWNER TO postgres;

--
-- Name: complaint_complaint_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.complaint_complaint_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.complaint_complaint_id_seq OWNER TO postgres;

--
-- Name: complaint_complaint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.complaint_complaint_id_seq OWNED BY public.complaint.complaint_id;


--
-- Name: complaint complaint_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint ALTER COLUMN complaint_id SET DEFAULT nextval('public.complaint_complaint_id_seq'::regclass);


--
-- Data for Name: complaint; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaint (complaint_id, category, complaint_text, summary, urgency, title, first_name, last_name, email, telephone, address, time_stamp, longitude, latitude) FROM stdin;
34	Highways, Traffic and Parking	Parking has become a significant issue on our street due to the influx of non-resident vehicles. This makes it difficult for residents to find parking spaces. The introduction of a residents-only parking scheme would help alleviate this problem. Can the council consider implementing such a scheme to prioritize parking for residents?	Parking issues due to non-resident vehicles, request for residents-only parking scheme.\n	3	Dr	Thomas	King	king@example.com	0208 210 9876	29 Willow Street, Greenwich, SE10 2MN	2024-03-17 22:58:29.812557	0.022094	51.491082
35	Housing	There has been an increase in anti-social behavior in our council estate, including noise disturbances and vandalism. This is creating an unsafe and unpleasant living environment. Can the council increase security measures and patrols to address these issues and improve safety for residents?	Increase in anti-social behavior in council estate, request for increased security measures.	4	Mr	Matthew 	Turner	turner@example.com	0208 098 7654	73 Ash Avenue, Greenwich, SE10 0QR	2024-01-15 23:06:25.321988	0.062949	51.459861
27	Adult Social Care	I am deeply concerned about the care of my elderly mother, Mrs. Linda Thompson, at her residence. She has been left without essential medication for several days, which is critical for her health. This situation is urgent and needs immediate attention to ensure her well-being. Immediate action is required to rectify this oversight and provide her with the necessary care.	Elderly resident, Mrs. Thompson, has been without essential medication for several days, putting her health at risk	5	Ms	Karen	Thompson	karenthompson@example.com	0987654321	27 Oak Drive, Greenwich, London SE10 3AB	2023-06-06 12:12:20.453214	0.007622	51.485294
28	Business	I would like to suggest that the parking regulations for small businesses in our area be reviewed. While not an immediate concern, more flexible parking options would greatly benefit business owners and customers alike. Please consider evaluating the current regulations to support local businesses.	Suggestion to review parking regulations for small businesses	3	Mr	Robert	Miller	robertmiller@example.com	1122334455	123 Commerce Street, Greenwich, London SE10 2XY	2024-06-06 12:12:54.825054	0.020847	51.48858
29	Business	The recent increase in fees for public parking has discouraged many residents from using local shops, leading to a decline in foot traffic and sales. Reviewing these fees could help revitalize the area's economy.	Increase in public parking fees affecting local shop sales	2	Mrs	Sophia	Wong	sophiawong@example.com	3344556677	456 Main Street, Greenwich, London SE10 4YZ	2024-06-06 12:15:34.07623	-0.015683	51.47599
30	Business	The recent closure of the main road due to ongoing construction works has severely impacted our business. With limited access and visibility, we are experiencing a significant decrease in customer traffic and sales. Urgent action is needed to address this issue and minimize further financial losses.	Business severely impacted by road closure, requiring immediate action to minimize financial losses	5	Mr	David	Smith	davidsmith@example.com	5566778899	789 Commercial Avenue, Greenwich, London SE10 6WX	2024-06-06 12:16:11.676703	-0.007667	51.47495
24	Adult Social Care	My father, Mr. John Smith, has been experiencing delays in receiving his prescribed medication through the adult social care services. While his condition is stable, timely delivery of his medication is crucial to maintaining his health. Could the process for medication delivery be reviewed to prevent future delays?	Delay in medication delivery for Mr. John Smith through adult social care services	3	Mr	David	Smith	davidsmith@example.com	1234567890	15 Elm Street, Greenwich, London SE10 9XY	2024-06-01 12:09:15.958046	0.007694	51.495587
7	Adult Social Care	My disabled brother has been waiting for a suitable wheelchair from the council for over three months now. Despite several follow-up calls and emails, we have not received any updates on the status of his request. This delay is causing significant inconvenience and affecting his mobility and quality of life. Can the council expedite this process and provide us with a definite timeline?	Three-month delay in providing wheelchair for disabled brother.	4	Mr	Jude	Smitt	smitt@example.com	0208 987 6543	34 Maple Avenue, Greenwich, SE10 8GH	2024-06-10 22:43:26.207296	0.090075	51.498805
3	Environment, Planning, Parks, Cemeteries and Waste	The rubbish collection service has been inconsistent for the past month. Our bins are often left uncollected, leading to overflowing trash and unpleasant smells.	Inconsistent rubbish collection service causing overflowing bins.	3	Mrs	Sarah	Johnston	sarahjohnston@example.com	0208 765 4321	56 Oak Lane, Greenwich, SE10 7HJ	2024-06-10 22:07:24.039668	0.108271	51.493889
23	Adult Social Care	The scheduling of home visits for my elderly mother, Mrs. Margaret Williams, at 42 Charlton Road, Greenwich, London SE7 7AB, has been inconsistent. While her essential needs are being met, more regular and timely visits would improve her overall well-being. Could the schedule be reviewed to ensure a more consistent service?	Inconsistent scheduling of home visits for elderly resident	3	Mrs	Sarah	Williams	sarahwilliams@example.com	3456789012	42 Charlton Road, Greenwich, London SE7 7AB	2024-06-06 12:00:00.567069	-0.005162	51.480982
26	Children's Services	I have noticed that my daughter, Emma Johnson, has not been receiving her scheduled speech therapy sessions regularly. While her development is progressing, consistent sessions are important for her continued improvement. I kindly request that the scheduling be reviewed to ensure she receives the necessary support without further interruptions.	Daughter's speech therapy sessions not being held regularly.	3	Mr	James	Johnson	jamesjohnson@example.com	2345678901	34 Pine Street, Greenwich, London SE10 5QW	2024-06-02 12:10:49.604549	0.024939	51.491532
1	Community Safety	The street lighting in our area is inadequate, making it difficult to see at night and increasing the risk of accidents and crime. Several lights are either broken or not bright enough. This is a serious safety concern that needs to be addressed immediately. Can the council inspect and repair the streetlights?	Inadequate street lighting, request for inspection and repair.	4	Ms	Jane	Doe	janedoe@example.com	0208 123 4567	12 Elm Street, Greenwich, SE10 9EF	2023-01-10 22:01:01.23456	0.115481	51.481062
9	Council Tax and Benefits	My council tax bill has increased significantly this year, yet I have not seen any corresponding improvement in local services. This increase is putting a strain on my finances. I would like an explanation from the council regarding the reasons for this hike and a review of the services provided to ensure we are getting value for our money.	Significant increase in council tax bill, no improvement in services.	2	Ms	Maria	Harris	harris@example.com	0208 987 6543	43 Chestnut Avenue, Greenwich, SE10 9YZ	2024-02-10 22:48:46.154934	0.035827	51.448516
32	GLLaB	The recent GLLaB job fair was poorly organized, with insufficient space for attendees and a lack of useful information for job seekers. This was a missed opportunity for both employers and job seekers. Can the council ensure better planning and execution for future events to make them more beneficial and accessible?	Poorly organized GLLaB job fair, insufficient space and information.	2	Mr	Joshua	Hall	hall@example.com	0208 432 1098	63 Cedar Lane, Greenwich, SE10 4IJ	2024-02-10 22:55:54.05647	0.02793	51.476971
33	Highways, Traffic and Parking	The new traffic lights at the junction near my house are causing long delays and confusion among drivers. The timing of the lights seems off, leading to traffic build-up and frustration. This issue needs to be addressed to improve traffic flow and safety in the area. Can the council review and adjust the timing of these traffic lights?	New traffic lights causing long delays and confusion, request for timing adjustment.	3	Mrs	Rebecca	Young	young@example.com	0208 321 0987	85 Elm Avenue, Greenwich, SE10 3KL	2024-03-01 22:58:29.812557	0.062606	51.470983
2	Highways, Traffic and Parking	There is a large pothole on our street that has been there for months. It has caused damage to several cars and poses a significant hazard to both drivers and pedestrians. Despite numerous complaints, no action has been taken. This issue requires urgent attention to prevent accidents and further damage.	Large pothole causing car damage and hazard, requires urgent repair.	5	Mr	John	Smith	johnsmith@example.com	0208 987 6543	34 Maple Avenue, Greenwich, SE10 8GH	2023-11-01 22:04:37.007937	0.016601	51.461359
4	Environment, Planning, Parks, Cemeteries and Waste	The park near my home is in a state of neglect. The grass is overgrown, there is litter everywhere, and the playground equipment is in disrepair. This is disappointing as the park is an important community space. Can the council take immediate steps to clean and maintain the park regularly to ensure it is safe and enjoyable for all residents?	Poor maintenance of local park, overgrown grass, litter, and damaged equipment.	3	Mr	Michael	Brown	michaelbrown@example.com	0208 654 3210	78 Pine Road, Greenwich, SE10 6KL	2023-08-10 22:09:08.489284	0.105178	51.501982
39	Adult Social Care	The recent increase in fees for public parking has discouraged many residents from using local shops, leading to a decline in foot traffic and sales. Reviewing these fees could help revitalize the area's economy	Increase in public parking fees affecting local shop sales	3	e	e	e	r	r	SE10 0AA	2024-06-24 16:55:36.686382	0.0033101	51.4871224
15	Highways, Traffic and Parking	The road markings at the roundabout near my house have faded significantly, causing confusion and near accidents as drivers are unsure of lane discipline. This is particularly hazardous during peak hours. Can the council repaint the road markings to improve safety and ensure smooth traffic flow?	Faded road markings at roundabout causing confusion, request for repainting.	4	Mr	Andrew	James	james@example.com	0208 432 5678	40 Oak Avenue, Greenwich, SE10 8GH	2023-06-10 23:37:11.825622	0.040977	51.483813
16	Highways, Traffic and Parking	There has been a persistent issue with illegal parking on our street, especially during weekends. This obstructs the road and makes it difficult for emergency vehicles to pass. Despite repeated complaints, no enforcement action has been taken. Can the council increase parking enforcement in the area to address this issue?	Illegal parking obstructing road, request for increased enforcement.	4	Mrs	Karen	Wilson	karen@example.com	0208 321 4567	77 Birch Road, Greenwich, SE10 9YZ\n\n	2023-12-10 23:37:11.825622	-0.010178	51.476971
11	Highways, Traffic and Parking	The speed bumps on our street are not effectively slowing down traffic. Many drivers continue to speed, creating a hazardous environment for pedestrians, especially children and the elderly. There have been near-miss incidents recently. Can the council consider installing more effective traffic calming measures, such as additional speed bumps or a reduced speed limit, to enhance safety?	Ineffective speed bumps, request for additional traffic calming measures.	4	Mrs	Sophie	Wilson	wilson@example.com	0208 543 2109	12 Fir Road, Greenwich, SE10 4IJ	2023-12-08 23:33:33.034289	-0.004685	51.482958
12	Highways, Traffic and Parking	The pedestrian crossing at the busy intersection near my home has malfunctioning signals. The walk signal often doesn't work, making it dangerous for pedestrians to cross the road safely. This is particularly concerning during school hours when many children use the crossing. Can the council urgently repair the signals to ensure pedestrian safety?	Malfunctioning pedestrian crossing signals, urgent repair needed.	5	Ms	Olive	Martin	martin@example.com	 0208 432 1098	35 Willow Lane, Greenwich, SE10 3KL	2023-07-10 23:33:33.034289	0.02999	51.484454
25	Children's Services	I am extremely concerned about the lack of immediate support for my son, Michael Brown, who has been showing signs of severe anxiety and depression. Despite multiple requests, we have not received the necessary intervention and counseling services. This situation is urgent as it directly affects his mental health and well-being. Immediate action is required to provide him with the support he needs.	Urgent concern for son's mental health and well-being, requiring immediate intervention and support	5	Mrs	Emily	Brown	emilybrown@example.com	9876543210	89 Maple Avenue, Greenwich, London SE10 8XY	2023-08-06 12:09:56.944537	0.014027	51.489651
5	Environment, Planning, Parks, Cemeteries and Waste	There are numerous abandoned vehicles on our street. They take up parking space and look unsightly. Can they be removed?	Abandoned vehicles on street taking up parking space.	3	Ms	Laura	Martinez	laura@example.com	0208 321 0987	45 Willow Lane, Greenwich, SE10 3QR\n\n	2023-07-19 22:38:58.797419	0.039603	51.462856
6	Community Safety	The playground equipment in the local park is damaged and unsafe for children. Please arrange for repairs or replacements.	Damaged playground equipment in local park, unsafe for children.	5	Mr	Robert 	Wilson	robert@example.com	0208 432 1098	23 Birch Avenue, Greenwich, SE10 4OP	2023-10-12 22:38:58.797419	0.04338	51.47269
20	Environment, Planning, Parks, Cemeteries and Waste	The hedge trimming in our local park was recently done, but the workers missed a small section near the entrance. While this isn't a major issue, it does look untidy compared to the rest of the park. Could the council arrange for the hedge trimming team to revisit and tidy up the missed section when they next perform maintenance in the park?	Missed section during hedge trimming in local park, request for tidy-up.	1	Mrs	Laura	Johnston	johnston@example.com	0208 765 1234	15 Maple Grove, Greenwich, SE10 5QR	2024-06-11 00:04:07.946546	0.091105	51.493248
8	Community Safety	There has been a recent increase in burglaries in our neighborhood, and residents are feeling unsafe. Despite multiple reports to the council, there has been no visible increase in police patrols or community safety measures. This situation needs urgent attention to prevent further incidents and ensure the safety of residents. Can the council take immediate action to enhance community safety?	Increase in burglaries, request for enhanced community safety measures.	5	Mrs	Elizabeth	White	white@example.com	0208 109 8765	89 Poplar Road, Greenwich, SE10 1UV	2024-01-11 22:46:57.577428	0.096598	51.487263
10	Council Tax and Benefits	I applied for housing benefits two months ago and have yet to receive any update on the status of my application. This delay is causing financial hardship as I am struggling to cover my rent. The council needs to expedite the processing of benefits applications and provide timely updates to applicants.	Two-month delay in housing benefits application, causing financial hardship.	4	Mr	Christopher	Clark	clark@example.com	0208 876 5432	65 Spruce Street, Greenwich, SE10 8BA	2024-01-20 22:50:31.862409	0.080802	51.487234
31	GLLaB	As a small business owner, I am struggling to find qualified local employees. The council's job placement services through GLLaB have not been effective in matching job seekers with available positions. Can the council improve the support and resources provided to local businesses to help us find suitable candidates more efficiently?	Ineffective job placement services through GLLaB, need better support for businesses.	3	Ms	Robin	Pattinson	pattinson@example.com	0208 543 2109	41 Redwood Avenue, Greenwich, SE10 5GH	2024-01-03 22:55:54.05647	0.063979	51.483386
13	Council Tax and Benefits	I recently discovered an error in my council tax bill, where I was overcharged for the past six months. Despite contacting the council multiple times, the issue has not been resolved, and I have not received any reimbursement. This overcharge is affecting my finances, and I need this issue resolved immediately. Can the council correct the billing error and process a refund as soon as possible?	Overcharged council tax bill for six months, request for correction and refund.	4	Mrs	Samantha	Brown	sambrown@example.com	0208 321 0987	49 Elm Street, Greenwich, SE10 9YZ\n\n	2023-09-10 23:33:33.034289	0.076682	51.477613
14	Council Tax and Benefits	The process of applying for council tax reduction has been extremely slow and cumbersome. Despite providing all required documents and information promptly, I have been waiting for over two months for a decision. This delay is causing financial strain. Can the council streamline the application process and expedite the review of my application?	Slow council tax reduction application process, request for expedited review.	3	Mr	Joshua	Barnet	barnet@example.com	 0208 109 8765	85 Ash Road, Greenwich, SE10 1UV\n	2023-10-10 23:33:33.034289	0.105178	51.477185
22	Adult Social Care	The care home where my father resides, which is managed by the council, has been experiencing staffing shortages. This has resulted in a decline in the quality of care, with residents not receiving timely assistance with daily activities. This situation is causing significant distress to my father and other residents. Can the council take immediate steps to address the staffing issues and ensure adequate care for the elderly?	Staffing shortages in care home leading to decline in quality of care.	5	Mr	Kevin	Harris	kevinharris@example.com	0208 765 4321	47 Maple Street, Greenwich, SE10 9EF	2024-05-30 23:28:41.782393	0.024497	51.477185
21	Adult Social Care	The Meals on Wheels service for my elderly neighbor has been inconsistent, with several missed deliveries in the past few weeks. This service is vital for her as she relies on it for her daily nutrition. Missed deliveries are not only inconvenient but also jeopardize her health. Can the council ensure that this essential service is reliable and that no further deliveries are missed?	Inconsistent Meals on Wheels service, several missed deliveries affecting elderly neighbor.	4	Ms	Emma	Taylor	emmataylor@example.com	0208 654 3210\n	61 Birch Avenue, Greenwich, SE10 8GH	2024-04-17 23:28:41.782393	0.038573	51.493219
17	Highways, Traffic and Parking	The recent installation of new parking meters in our area has been problematic. The meters frequently malfunction, and the payment app is unreliable. This has led to numerous parking fines for residents despite our attempts to pay. Can the council fix these technical issues and provide a more reliable system for parking payments?	Malfunctioning parking meters and unreliable payment app causing fines.	3	Mr	Ben	Carter	carter@example.com	0208 109 8765	88 Ash Avenue, Greenwich, SE10 1UV	2023-10-10 23:37:11.825622	0.055053	51.460289
18	Council Tax and Benefits	I recently moved into a new property and applied for a single-person discount on my council tax. Despite submitting all necessary documentation over a month ago, I have yet to receive any confirmation or update from the council. This delay is causing unnecessary financial stress. Can the council expedite the processing of my discount application and provide an update on its status?	Delay in processing single-person council tax discount application.	3	Ms	Natalie	Cooper	cooper@example.com	0208 210 6543	22 Sycamore Lane, Greenwich, SE10 8EF	2023-09-10 23:39:59.517797	0.075652	51.457508
19	Council Tax and Benefits	My elderly mother, who is on a fixed income, has been struggling to get a council tax rebate. She has applied multiple times, but each application seems to get lost in the system, and she receives no feedback. This is causing her significant distress. Can the council provide clear guidance on the application process and ensure her application is reviewed promptly?	Elderly mother's council tax rebate applications repeatedly lost, needs prompt review.	4	Mr	Paul	Roberts	roberts@example.com	0208 987 1234	53 Pine Street, Greenwich, SE10 6GH	2023-11-11 23:39:59.517797	0.03514	51.462856
\.


--
-- Name: complaint_complaint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.complaint_complaint_id_seq', 40, true);


--
-- Name: complaint complaint_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint
    ADD CONSTRAINT complaint_pkey PRIMARY KEY (complaint_id);


--
-- PostgreSQL database dump complete
--

