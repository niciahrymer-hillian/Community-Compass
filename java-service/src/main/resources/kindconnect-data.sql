DELETE FROM resource;
INSERT INTO resource (name, category, description, location, phone)
VALUES
-- Food
('Community Food Center', 'Food', 'Provides food boxes and meal support for families.', 'Wilmington, DE', '302-000-0001'),
('Local Food Bank', 'Food', 'Offers free groceries and emergency food assistance.', 'Newark, DE', '302-000-0002'),
('Weekend Grocery Pantry', 'Food', 'Offers weekend grocery pickup and emergency food boxes.', 'Middletown, DE', '302-000-0003'),
('Neighborhood Meal Program', 'Food', 'Provides hot meals for seniors and families.', 'Dover, DE', '302-000-0004'),
('Family Nutrition Support', 'Food', 'Helps families find affordable nutrition and meal support.', 'New Castle, DE', '302-000-0005'),
('Baltimore Food Pantry', 'Food', 'Provides groceries and emergency meal support.', 'Baltimore, MD', '410-000-0006'),
('Silver Spring Meal Center', 'Food', 'Offers meal programs and food support for families.', 'Silver Spring, MD', '301-000-0007'),
('Philadelphia Community Pantry', 'Food', 'Provides food boxes and pantry support.', 'Philadelphia, PA', '215-000-0008'),
('South Philly Meal Help', 'Food', 'Offers meal support and grocery referrals.', 'South Philadelphia, PA', '215-000-0009'),
('Chester Food Support Center', 'Food', 'Provides emergency food support and referrals.', 'Chester, PA', '610-000-0010'),

-- Healthcare
('Free Health Clinic', 'Healthcare', 'Provides basic health checkups and medical support.', 'Wilmington, DE', '302-000-0011'),
('Community Wellness Clinic', 'Healthcare', 'Offers low-cost health services and wellness support.', 'Dover, DE', '302-000-0012'),
('Senior Health Support Center', 'Healthcare', 'Helps seniors find health screenings and wellness programs.', 'Newark, DE', '302-000-0013'),
('Mental Wellness Resource Center', 'Healthcare', 'Provides emotional wellness and counseling support information.', 'Wilmington, DE', '302-000-0014'),
('Family Care Clinic', 'Healthcare', 'Offers basic care support for families and caregivers.', 'Middletown, DE', '302-000-0015'),
('Baltimore Community Clinic', 'Healthcare', 'Provides basic healthcare and community health referrals.', 'Baltimore, MD', '410-000-0016'),
('Rockville Wellness Center', 'Healthcare', 'Offers wellness programs and health support information.', 'Rockville, MD', '301-000-0017'),
('Philadelphia Health Resource Center', 'Healthcare', 'Connects users with local health and clinic resources.', 'Philadelphia, PA', '215-000-0018'),
('Upper Darby Family Clinic', 'Healthcare', 'Provides family healthcare support and referrals.', 'Upper Darby, PA', '610-000-0019'),
('Norristown Wellness Help', 'Healthcare', 'Offers wellness information and health resource support.', 'Norristown, PA', '610-000-0020'),

-- Transportation
('Ride Support Program', 'Transportation', 'Helps people find transportation for appointments and errands.', 'New Castle, DE', '302-000-0021'),
('Senior Ride Service', 'Transportation', 'Provides ride help for seniors and caregivers.', 'Middletown, DE', '302-000-0022'),
('Medical Appointment Rides', 'Transportation', 'Connects users with ride options for doctor visits.', 'Wilmington, DE', '302-000-0023'),
('Community Shuttle Information', 'Transportation', 'Shares local shuttle and bus support information.', 'Dover, DE', '302-000-0024'),
('Caregiver Transportation Help', 'Transportation', 'Supports caregivers who need transportation options.', 'Newark, DE', '302-000-0025'),
('Baltimore Ride Help', 'Transportation', 'Helps users find rides for appointments and errands.', 'Baltimore, MD', '410-000-0026'),
('Annapolis Transportation Support', 'Transportation', 'Provides transportation resource information.', 'Annapolis, MD', '410-000-0027'),
('Philadelphia Ride Resource Desk', 'Transportation', 'Connects users with local ride support options.', 'Philadelphia, PA', '215-000-0028'),
('Bensalem Community Rides', 'Transportation', 'Provides ride support information for local residents.', 'Bensalem, PA', '215-000-0029'),
('Media Medical Ride Help', 'Transportation', 'Helps users find rides to healthcare appointments.', 'Media, PA', '610-000-0030'),

-- Caregiver Support
('Caregiver Support Group', 'Caregiver Support', 'Support group and information for caregivers and families.', 'Wilmington, DE', '302-000-0031'),
('Family Support Center', 'Caregiver Support', 'Helps families with care planning and community support.', 'Newark, DE', '302-000-0032'),
('Respite Care Information Center', 'Caregiver Support', 'Helps caregivers find short-term care support options.', 'Dover, DE', '302-000-0033'),
('Care Planning Help Desk', 'Caregiver Support', 'Guides families through basic care planning and local service options.', 'New Castle, DE', '302-000-0034'),
('Parent and Family Support Line', 'Caregiver Support', 'Provides information and emotional support for family caregivers.', 'Middletown, DE', '302-000-0035'),
('Baltimore Caregiver Network', 'Caregiver Support', 'Connects caregivers with support groups and resources.', 'Baltimore, MD', '410-000-0036'),
('Silver Spring Family Support', 'Caregiver Support', 'Provides care planning and caregiver support information.', 'Silver Spring, MD', '301-000-0037'),
('Philadelphia Caregiver Help Center', 'Caregiver Support', 'Supports caregivers with information and local resources.', 'Philadelphia, PA', '215-000-0038'),
('Chester Family Care Support', 'Caregiver Support', 'Helps families find caregiver and respite support.', 'Chester, PA', '610-000-0039'),
('Upper Darby Care Planning Desk', 'Caregiver Support', 'Provides caregiver planning and family support resources.', 'Upper Darby, PA', '610-000-0040'),

-- Shelter
('Community Shelter Help', 'Shelter', 'Connects people with temporary housing and shelter support.', 'Dover, DE', '302-000-0041'),
('Emergency Housing Line', 'Shelter', 'Provides information for emergency housing help.', 'Wilmington, DE', '302-000-0042'),
('Family Shelter Resource Center', 'Shelter', 'Helps families find temporary shelter and housing support services.', 'Newark, DE', '302-000-0043'),
('Safe Housing Support', 'Shelter', 'Connects people with safe temporary housing information.', 'New Castle, DE', '302-000-0044'),
('Temporary Housing Help Desk', 'Shelter', 'Provides shelter referrals and temporary housing information.', 'Middletown, DE', '302-000-0045'),
('Baltimore Shelter Support', 'Shelter', 'Connects users with local shelter and housing resources.', 'Baltimore, MD', '410-000-0046'),
('Rockville Emergency Housing', 'Shelter', 'Provides emergency housing and shelter information.', 'Rockville, MD', '301-000-0047'),
('Philadelphia Shelter Resource Center', 'Shelter', 'Helps users find temporary housing support.', 'Philadelphia, PA', '215-000-0048'),
('South Philly Housing Help', 'Shelter', 'Connects families with local shelter information.', 'South Philadelphia, PA', '215-000-0049'),
('Norristown Safe Housing Desk', 'Shelter', 'Provides temporary housing and shelter referrals.', 'Norristown, PA', '610-000-0050'),

-- Accessibility
('Accessibility Resource Center', 'Accessibility', 'Provides information for disability support and accessibility services.', 'New Castle, DE', '302-000-0051'),
('Mobility Equipment Support', 'Accessibility', 'Helps users find walkers, wheelchairs, and mobility support tools.', 'Newark, DE', '302-000-0052'),
('Disability Services Help Desk', 'Accessibility', 'Guides users to disability services and accessibility programs.', 'Wilmington, DE', '302-000-0053'),
('Accessible Transportation Info', 'Accessibility', 'Provides information about accessible ride and transportation options.', 'Dover, DE', '302-000-0054'),
('Home Accessibility Support', 'Accessibility', 'Connects users with home accessibility resource information.', 'Middletown, DE', '302-000-0055'),
('Baltimore Accessibility Desk', 'Accessibility', 'Provides disability support and accessibility referrals.', 'Baltimore, MD', '410-000-0056'),
('Silver Spring Mobility Help', 'Accessibility', 'Helps users find mobility and accessibility support.', 'Silver Spring, MD', '301-000-0057'),
('Philadelphia Disability Resource Center', 'Accessibility', 'Connects users with disability support programs.', 'Philadelphia, PA', '215-000-0058'),
('Bensalem Accessibility Help', 'Accessibility', 'Provides accessibility and mobility support information.', 'Bensalem, PA', '215-000-0059'),
('Media Assistive Support Desk', 'Accessibility', 'Offers assistive technology and accessibility information.', 'Media, PA', '610-000-0060'),

-- Community Services
('Local Community Services', 'Community Services', 'Connects people with local programs and general support services.', 'Middletown, DE', '302-000-0061'),
('Community Help Desk', 'Community Services', 'Guides people to different local support programs.', 'Wilmington, DE', '302-000-0062'),
('Family Resource Network', 'Community Services', 'Connects families with community support and basic needs programs.', 'Newark, DE', '302-000-0063'),
('Senior Community Center', 'Community Services', 'Provides community programs and support information for seniors.', 'Dover, DE', '302-000-0064'),
('Neighborhood Support Office', 'Community Services', 'Helps residents find local community programs and support services.', 'New Castle, DE', '302-000-0065'),
('Baltimore Community Help Desk', 'Community Services', 'Connects residents with support programs and referrals.', 'Baltimore, MD', '410-000-0066'),
('Annapolis Family Resource Center', 'Community Services', 'Provides family and community support information.', 'Annapolis, MD', '410-000-0067'),
('Philadelphia Community Support Office', 'Community Services', 'Helps residents find local support programs.', 'Philadelphia, PA', '215-000-0068'),
('West Philly Community Help', 'Community Services', 'Provides local community resource referrals.', 'West Philadelphia, PA', '215-000-0069'),
('Chester Neighborhood Services', 'Community Services', 'Connects people with community support services.', 'Chester, PA', '610-000-0070'),

-- Tech Help
('Digital Skills Help Desk', 'Tech Help', 'Helps users with phones, computers, email, and basic technology.', 'Wilmington, DE', '302-000-0071'),
('Senior Tech Help', 'Tech Help', 'Supports seniors with phones, video calls, and online forms.', 'Newark, DE', '302-000-0072'),
('Community Tech Support', 'Tech Help', 'Provides basic technology help and digital guidance.', 'Dover, DE', '302-000-0073'),
('Phone Setup Support', 'Tech Help', 'Helps users set up phones, apps, and accounts.', 'New Castle, DE', '302-000-0074'),
('Online Access Help', 'Tech Help', 'Guides users with internet access and online services.', 'Middletown, DE', '302-000-0075'),
('Baltimore Digital Help', 'Tech Help', 'Provides technology help for phones and computers.', 'Baltimore, MD', '410-000-0076'),
('Rockville Tech Support Desk', 'Tech Help', 'Helps users with basic digital skills and devices.', 'Rockville, MD', '301-000-0077'),
('Philadelphia Community Tech Help', 'Tech Help', 'Supports users with devices, email, and online services.', 'Philadelphia, PA', '215-000-0078'),
('South Philly Device Help', 'Tech Help', 'Helps residents with phones, computers, and apps.', 'South Philadelphia, PA', '215-000-0079'),
('Norristown Digital Support', 'Tech Help', 'Provides basic tech help and online access guidance.', 'Norristown, PA', '610-000-0080'),

-- Friendly Call
('Friendly Call Program', 'Friendly Call', 'Connects users with volunteers for friendly phone conversations.', 'Wilmington, DE', '302-000-0081'),
('Companion Call Support', 'Friendly Call', 'Provides social check-in calls for people feeling lonely.', 'Newark, DE', '302-000-0082'),
('Community Listening Line', 'Friendly Call', 'Offers supportive listening and friendly conversation.', 'Dover, DE', '302-000-0083'),
('Senior Check-In Calls', 'Friendly Call', 'Provides regular check-in calls for seniors.', 'New Castle, DE', '302-000-0084'),
('Wellness Call Network', 'Friendly Call', 'Connects users with caring volunteers for phone support.', 'Middletown, DE', '302-000-0085'),
('Baltimore Friendly Call Line', 'Friendly Call', 'Offers friendly phone calls and check-ins.', 'Baltimore, MD', '410-000-0086'),
('Silver Spring Companion Calls', 'Friendly Call', 'Connects people with supportive conversation volunteers.', 'Silver Spring, MD', '301-000-0087'),
('Philadelphia Listening Line', 'Friendly Call', 'Provides friendly calls and emotional support referrals.', 'Philadelphia, PA', '215-000-0088'),
('Upper Darby Check-In Calls', 'Friendly Call', 'Offers social check-ins and friendly conversations.', 'Upper Darby, PA', '610-000-0089'),
('Media Friendly Call Support', 'Friendly Call', 'Connects users with volunteers for phone conversations.', 'Media, PA', '610-000-0090');

