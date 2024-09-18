connection: "external_small"

### Owner - Tal ###

include: "/**/*.view.lkml"          # include all views in this project
include: "/**/*.dashboard.lookml"   # include a LookML dashboard called my_dashboard

week_start_day: sunday

# Explores
# Policy Checkout Details
explore: model_1 {
access_filter: {field: dima_table.merchant
                  user_attribute: merchant_id}
access_filter: {
     field: user_attribute_test.email
     user_attribute: email
   }


}

explore: user_attribute_test {
  fields: [ALL_FIELDS*]
   access_filter: {
     field: user_attribute_test.merchant
     user_attribute: merchant_id
   }
}