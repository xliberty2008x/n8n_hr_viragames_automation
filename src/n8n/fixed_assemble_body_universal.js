/* ───── helpers ──────────────────────────────────────────────────────── */
const isoCountry = (label) => ({
  Ukraine: 'UA',
  Poland : 'PL',
  Germany: 'DE',
  'United States': 'US',
}[label] || label);                 // fallback: use the label itself

/* ───── gather inputs ───────────────────────────────────────────────── */
// Get data from the simplified schema of Get Database Page by Id
const pageData = $('Get Database Page by Id').first().json;

/* Notion look‑ups already performed upstream */
const deptNode  = $('Find Department page').first().json;
const roleNode  = $('Find Role page').first().json;
const teamNode  = $('Find Team page').first().json;
const userNode  = $('convert to json object4').first().json;

/* IDs & names */
const ttId   = pageData.property_tt_requisition_id?.trim() || null;
const isUpdate = !!ttId;                           // ← create vs update

const departmentId = deptNode?.property_tt_department_id?.trim() || null;
const roleId       = roleNode?.property_tt_role_id?.trim()         || null;
const teamName     = teamNode?.name                                || null;
const userId       = userNode?.data?.[0]?.id?.trim()               || null;

/* ───── salary logic ───────────────────────────────────────────────── */
const wantRange = pageData.property_need_salary_range ?? true;
let minSalary   = null;
let maxSalary   = null;

if (wantRange) {
  minSalary = pageData.property_min_salary ?? null;
  maxSalary = pageData.property_max_salary ?? null;
} else {
  const fixed = pageData.property_fixed_salary ?? null;
  if (fixed !== null) {
    minSalary = fixed - 1;      // TT requires both even if equal
    maxSalary = fixed;
  }
}

/* ───── relationships ──────────────────────────────────────────────── */
const relationships = {
  location:  { data: { id: '1200146', type: 'locations'  } },  // constant
};
if (departmentId) relationships.department = { data: { id: departmentId, type: 'departments' } };
if (roleId)       relationships.role       = { data: { id: roleId,       type: 'roles'       } };
if (userId)       relationships.user       = { data: { id: userId,       type: 'users'       } };

/* ───── extract date values ─────────────────────────────────────────── */
const desireStartDate = pageData.property_desire_start_day_of_newcomer?.start ?? null;

/* ───── payload ─────────────────────────────────────────────────────── */
const payload = {
  data: {
    type: 'requisitions',
    ...(isUpdate ? { id: ttId } : {}),            // add id only on update
    attributes: {
      'job-title':          pageData.property_name ?? '',
      'job-description':    pageData.property_job_description ?? '',
      country:              isoCountry(pageData.property_country ?? ''),
      'min-salary':         minSalary,
      'max-salary':         maxSalary,
      currency:             'USD',
      'salary-time-unit':   (pageData.property_salary_period ?? '').toLowerCase(),
      'number-of-openings': pageData.property_expected_number_of_hires ?? null,
      'custom-form-answers': {
        desire_start_day:       desireStartDate,
        priority_of_position:   pageData.property_priority_of_position ?? null,
        level_of_candidate:     pageData.property_level_of_candidate ?? null,
        team:                   teamName,
        reason:                 Array.isArray(pageData.property_reason) ? pageData.property_reason.join(', ') : (pageData.property_reason ?? ''),
        will_there_be_a_test_task:
                                 pageData.property_will_there_be_a_test_task ?? null,
        please_define_hiring_stages:
                                 pageData.property_please_define_hiring_stages ?? '',
        key_competencies_for_position:
                                 pageData.property_key_competencies_for_position ?? '',
        additional_comments_for_recruiter_or_approval:
                                 pageData.property_additional_comments_for_recruiter_or_approval ?? ''
      },
      status: 'pending'
    },
    relationships
  }
};

/* ───── output ──────────────────────────────────────────────────────── */
return {
  payload,
  isUpdate,
  ttId,
};